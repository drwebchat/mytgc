# app.py
import streamlit as st
import subprocess
import os
import tempfile
import json

st.title("TGCF Forwarder Control Panel")

st.write("Configure your Telegram bot forwarding parameters.")

bot_token = st.text_input("Bot Token", type="password")
source_chat = st.text_input("Source Chat ID")
dest_chat = st.text_input("Destination Chat ID")

if st.button("Start Forwarding"):
    if not all([bot_token, source_chat, dest_chat]):
        st.error("Please fill in all fields.")
    else:
        st.success("Starting tgcf forwarding...")

        # Create temporary tgcf config
        config = {
            "forwards": [
                {"source": source_chat, "dest": dest_chat}
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(config, f)
            config_path = f.name

        os.environ["TGCF_TELEGRAM_BOT_TOKEN"] = bot_token

        # Run tgcf as subprocess
        st.write("Running tgcf... (logs below)")
        process = subprocess.Popen(["tgcf", "--config", config_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)

        for line in process.stdout:
            st.write(line)
