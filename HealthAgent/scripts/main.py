# main.py - Flask backend
from flask import Flask, request, jsonify, render_template
from logic import analyze
from input import save_data, load_data, convert_export_to_daily
import json
import os
import queue
import threading

# ─── Queue ─────────────────────────────────────────────
event_queue = queue.Queue()

# ─── App ───────────────────────────────────────────────

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

# ── Directories ─────────────────────────────────────────

MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'memory')
COMM_DIR = os.path.join(os.path.dirname(__file__), '..', 'communication')
DATA_FILE = os.path.join(MEMORY_DIR, 'data.json')
GOALS_FILE = os.path.join(MEMORY_DIR, 'goals.json')
ALERT_FILE = os.path.join(COMM_DIR, 'alert.json')

# ── Routes ──────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def receive_data():
    # Health Auto Export will POST data here
    data = request.json

    print("RAW EXPORT DATA:", json.dumps(data, indent=2))
    print("Received data: ", data)
    
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    
    data = json.loads(json.dumps(data, indent=2))
    if "data" in data and "metrics" in data.get("data", {}):
        conversion = convert_export_to_daily(data)
        for entry in conversion:
            save_data(entry)

        event_queue.put({"event": "export_received"})

    else:
        save_data(data)
    
    return jsonify({"status": "ok"}), 200

@app.route('/advice', methods=['GET'])
def get_advice():
    try:
        recommendations, report_type = analyze()
        return jsonify({
            "report_type": report_type,
            "advice": recommendations
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()  # prints the full error to the terminal
        return jsonify({"error": str(e)}), 500
    
@app.route('/goals', methods=['GET'])
def get_goals():
    try:
        with open(GOALS_FILE, 'r') as f:
            goals = json.load(f)
        return jsonify(goals), 200
    except:
        return jsonify({}), 200

@app.route('/goals', methods=['POST'])
def set_goals():
    goals = request.json
    print("Received goals: ", goals)
    if not goals:
        return jsonify({"error": "No goals received"}), 400
    with open(GOALS_FILE, 'w') as f:
        json.dump(goals, f, indent=4)
    print("Wrote to:", GOALS_FILE)
    return jsonify({"status": "ok"}), 200

@app.route('/history', methods=['GET'])
def get_history():
    data = load_data()
    return jsonify(data), 200

@app.route('/check-date', methods=['GET'])
def check_date():
    date = request.args.get("date")
    data = load_data()
    date_exists = any(entry.get("date") == date for entry in data)
    return jsonify({'exists': date_exists}), 200

@app.route('/data/<date>', methods = ['DELETE'])
def delete_data(date):
    data = load_data()
    new_data = []
    for entry in data:
        if entry.get("date") != date:
            new_data.append(entry)
    data = new_data
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent= 4)
    return jsonify({"status": "deleted"}), 200

@app.route('/stream')
def stream():
    # Server sent events
    def generate():
        while True:
            message = event_queue.get()
            print(f"data: {json.dumps(message)}\n\n")
            yield f"data: {json.dumps(message)}\n\n"
    print("***********************STREAM HAS RUN")
    return app.response_class(
        generate(),
        mimetype= 'text/event-stream',
        headers= {
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


# ── Run ─────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5000, host= '0.0.0.0', threaded = True)