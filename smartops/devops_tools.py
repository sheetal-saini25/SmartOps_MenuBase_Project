import time
import paramiko
import pandas as pd
import streamlit as st
from smartops.utils import show_page_header, DOCKER_AVAILABLE

# -----------------------------
# SSH Command Execution
# -----------------------------
def execute_ssh_command_with_stream(client, command):
    transport = client.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    channel.exec_command(command)
    output = []
    while True:
        if channel.exit_status_ready():
            break
        if channel.recv_ready():
            data = channel.recv(1024).decode('utf-8')
            output.append(data); yield data
        if channel.recv_stderr_ready():
            error = channel.recv_stderr(1024).decode('utf-8')
            output.append(f"[ERROR] {error}"); yield f"[ERROR] {error}"
    while channel.recv_ready():
        data = channel.recv(1024).decode('utf-8')
        output.append(data); yield data
    while channel.recv_stderr_ready():
        error = channel.recv_stderr(1024).decode('utf-8')
        output.append(f"[ERROR] {error}"); yield f"[ERROR] {error}"
    channel.close()

def execute_docker_command(ssh_client, command):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(f"docker {command}", get_pty=True)
        output = []
        while True:
            if stdout.channel.recv_ready():
                chunk = stdout.channel.recv(1024).decode('utf-8'); output.append(chunk)
            if stdout.channel.recv_stderr_ready():
                error = stdout.channel.recv_stderr(1024).decode('utf-8'); output.append(f"[ERROR] {error}")
            if stdout.channel.exit_status_ready():
                break
        exit_status = stdout.channel.recv_exit_status()
        return exit_status, "".join(output)
    except Exception as e:
        return 1, f"[ERROR] Failed to execute Docker command: {str(e)}"

# -----------------------------
# Docker Manager UI
# -----------------------------
def docker_manager_ui(ssh_client):
    st.header("🐳 Docker Container Manager (SSH)")
    if not ssh_client:
        st.warning("⚠️ SSH not connected.")
        return

    if 'docker_available' not in st.session_state:
        exit_status, _ = execute_docker_command(ssh_client, "--version")
        st.session_state.docker_available = (exit_status == 0)

    if not st.session_state.docker_available:
        st.error("❌ Docker not found on remote or no permission.")
        return

    command_type = st.radio("Select command type:", ["Container Management","Image Management","System Info","Custom Command"], horizontal=True)

    if command_type == "Container Management":
        _, out = execute_docker_command(ssh_client, "ps -a --format '{{.Names}}|{{.Image}}|{{.Status}}|{{.Ports}}'")
        containers = []
        for line in out.strip().splitlines():
            if not line.strip(): continue
            parts = line.split('|')
            if len(parts) < 4: continue
            name, image, status, ports = parts
            containers.append({"name":name,"image":image,"status":status,"ports":ports})

        if containers:
            st.subheader("📦 Containers")
            st.dataframe(pd.DataFrame(containers), use_container_width=True)
            selected = st.selectbox("Select a container:", [c["name"] for c in containers])
            c1,c2,c3,c4 = st.columns(4)
            if c1.button("▶️ Start"): st.code(execute_docker_command(ssh_client, f"start {selected}")[1])
            if c2.button("⏹️ Stop"): st.code(execute_docker_command(ssh_client, f"stop {selected}")[1])
            if c3.button("📜 Logs"):
                _, logs = execute_docker_command(ssh_client, f"logs {selected}")
                st.code(logs, language="bash")
            if c4.button("🗑️ Remove"): st.code(execute_docker_command(ssh_client, f"rm -f {selected}")[1])

        else:
            st.info("No containers found.")

    elif command_type == "Image Management":
        st.subheader("🖼️ Docker Images")
        _, out = execute_docker_command(ssh_client, "images --format '{{.Repository}}:{{.Tag}}|{{.Size}}'")
        images = []
        for line in out.strip().splitlines():
            if line.strip() and "<none>" not in line:
                name, size = line.split('|',1); images.append({"name":name,"size":size})
        if images: st.dataframe(pd.DataFrame(images), use_container_width=True)
        else: st.info("No Docker images found.")

    elif command_type == "System Info":
        st.subheader("Version"); _, v = execute_docker_command(ssh_client, "--version"); st.code(v, language="bash")
        st.subheader("System Info"); _, inf = execute_docker_command(ssh_client, "info"); st.code(inf, language="bash")

    else:
        custom_cmd = st.text_area("Enter Docker command (without 'docker'):", "ps -a")
        if st.button("🚀 Execute"):
            _, out = execute_docker_command(ssh_client, custom_cmd)
            st.subheader("Command Output"); st.code(out, language="bash")

# -----------------------------
# Main DevOps Tools
# -----------------------------
def show_devops_tools():
    show_page_header("🛠️ DevOps Tools")

    if not DOCKER_AVAILABLE:
        st.warning("⚠️ Python docker package not installed (only needed if using Docker SDK locally).")

    if 'ssh_client' not in st.session_state: st.session_state.ssh_client = None

    st.header("💻 SSH Client (Localhost/Linux IP)")
    with st.form("ssh_connection"):
        ssh_host = st.text_input("Linux Host/IP", value="127.0.0.1")
        ssh_username = st.text_input("Username", value="root")
        ssh_password = st.text_input("Password", type="password")
        connect_btn = st.form_submit_button("🔗 Connect")
        if connect_btn:
            try:
                if st.session_state.ssh_client: st.session_state.ssh_client.close()
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    hostname=ssh_host,
                    username=ssh_username,
                    password=ssh_password,
                    timeout=10,
                    look_for_keys=False,
                    allow_agent=False
                )
                st.session_state.ssh_client = client
                st.success(f"✅ Connected to {ssh_host}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Connection failed: {e}")
                st.session_state.ssh_client = None

    if st.session_state.ssh_client:
        st.success("🔗 SSH Connected")
        docker_manager_ui(st.session_state.ssh_client)
