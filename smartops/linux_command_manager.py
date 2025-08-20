import streamlit as st
from smartops.utils import show_page_header
import time, paramiko

def show_linux_command_manager():
    show_page_header("🐧 Linux Command Manager")

    # Session state
    if 'ssh_client' not in st.session_state: st.session_state.ssh_client = None
    if 'ssh_output' not in st.session_state: st.session_state.ssh_output = ""
    if 'command_running' not in st.session_state: st.session_state.command_running = False

    # SSH Connection Form
    with st.expander("🔑 SSH Connection", expanded=st.session_state.ssh_client is None):
        with st.form("ssh_connection_linux"):
            ssh_host = st.text_input("Server IP", placeholder="e.g., 192.168.1.10")
            ssh_username = st.text_input("Username", value="root")
            ssh_password = st.text_input("Password", type="password")
            connect_btn = st.form_submit_button("🔗 Connect")

            if connect_btn:
                if not ssh_host or not ssh_username or not ssh_password:
                    st.warning("⚠️ Please fill in all SSH details.")
                else:
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
                        st.session_state.ssh_output = ""
                        st.success(f"✅ Connected to {ssh_host} as {ssh_username}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ SSH connection failed: {str(e)}")
                        st.session_state.ssh_client = None

    # Linux Command Execution
    if st.session_state.ssh_client:
        st.success("🔗 Connected")
        with st.form("ssh_cmd_linux"):
            cmd = st.text_area("Enter Linux command to execute", "uname -a")
            run = st.form_submit_button("🚀 Execute")
            if run and cmd:
                holder = st.empty()
                full = []
                try:
                    stdin, stdout, stderr = st.session_state.ssh_client.exec_command(cmd)
                    for line in iter(stdout.readline, ""):
                        full.append(line)
                        holder.code(''.join(full), language="bash")
                        time.sleep(0.05)
                    err = stderr.read().decode()
                    if err:
                        st.error(f"❌ Error: {err}")
                except Exception as e:
                    st.error(f"❌ Command execution failed: {e}")
    else:
        st.info("ℹ️ Please connect to an SSH server to execute Linux commands.")
