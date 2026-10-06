class SubmissionSocket {
  constructor(url) {
    this.url = url || CONFIG.WS_URL;
    this.ws = null;
    this.listeners = new Map();
  }

  connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (this.listeners.has(payload.submissionId)) {
          this.listeners.get(payload.submissionId)(payload.data);
        }
      } catch (e) {
        console.error('WebSocket parse error:', e);
      }
    };
  }

  subscribe(submissionId, callback) {
    this.listeners.set(submissionId, callback);
  }
}

const submissionSocket = new SubmissionSocket();
