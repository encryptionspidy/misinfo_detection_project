from flask import Flask, request, jsonify
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('user_report_handler.log'), logging.StreamHandler()]
)

app = Flask(__name__)
DATA_FILE = 'user_reports.json'

@app.route('/report', methods=['POST'])
def handle_report():
    try:
        report = request.json
        if not report or 'content' not in report or 'source' not in report:
            logging.warning("Invalid report received.")
            return jsonify({"error": "Invalid report format."}), 400
        
        save_report(report)
        logging.info(f"Received report from {report['source']}")
        return jsonify({"status": "Report received successfully."}), 200

    except Exception as e:
        logging.error(f"Error handling user report: {e}")
        return jsonify({"error": "Internal server error."}), 500

def save_report(report):
    try:
        with open(DATA_FILE, 'a') as f:
            json.dump(report, f)
            f.write('\n')
    except Exception as e:
        logging.error(f"Error saving report: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
