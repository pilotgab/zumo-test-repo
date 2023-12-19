from flask import Flask, render_template, jsonify
import sqlite3
import logging
import os
import socket
from kubernetes import client, config

# Initialize Flask app
app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the base URL for the CDN for static files
app.config['CDN_URL'] = 'https://dapdex30lwsoy.cloudfront.net'

# Initialize and populate SQLite database
def init_db():
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (content TEXT)''')
        cursor.execute("INSERT INTO messages (content) VALUES ('Hello from Kubernetes!')")
        conn.commit()

init_db()

def get_kubernetes_info():
    logger.info("get_kubernetes_info function called")

    k8s_service_host = os.environ.get('KUBERNETES_SERVICE_HOST')
    k8s_service_path = '/var/run/secrets/kubernetes.io/serviceaccount'

    if k8s_service_host and os.path.isdir(k8s_service_path):
        logger.info("Detected Kubernetes environment")
        logger.info(f"KUBERNETES_SERVICE_HOST: {k8s_service_host}")
        try:
            config.load_incluster_config()
            v1 = client.CoreV1Api()
            pod_name = os.environ.get('HOSTNAME')
            namespace = 'zumo-test'  # Fixed namespace
            pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            logger.info(f"Pod name: {pod_name}, Pod IP: {pod.status.pod_ip}, Namespace: {namespace}")
            return {
                'pod_name': pod_name,
                'pod_ip': pod.status.pod_ip,
                'namespace': namespace,
                'kubernetes_api': k8s_service_host
            }
        except Exception as e:
            logger.exception("Failed to fetch Kubernetes info: {}".format(e))
            return None
    else:
        logger.info("Not running in a Kubernetes environment. Using mock data.")
        return {
            'pod_name': "MockPod",
            'pod_ip': "127.0.0.1",
            'namespace': "default",
            'kubernetes_api': "Mock API"
        }

# Route for Kubernetes info
@app.route('/api/kubernetes-info')
def kubernetes_info():
    logger.info("Accessing /api/kubernetes-info route")
    info = get_kubernetes_info()
    if info:
        return jsonify(info)
    else:
        return jsonify({'error': 'Not running in a Kubernetes environment'}), 404

# Home page route
@app.route('/')
def home():
    info = get_kubernetes_info()
    return render_template('index.html', info=info, cdn_url=app.config['CDN_URL'])

# API route for dynamic message
@app.route('/api/message')
def dynamic_message():
    try:
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM messages ORDER BY ROWID DESC LIMIT 1")
            message = cursor.fetchone()[0]
            return jsonify(message=message)
    except Exception as e:
        logger.exception("Failed to fetch message: {}".format(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# API route for server info
@app.route('/api/server-info')
def server_info():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return jsonify({
            'hostname': host_name,
            'ip': host_ip
        })
    except Exception as e:
        logger.exception("Failed to fetch server info: {}".format(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)