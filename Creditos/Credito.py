import streamlit as st

def display_credits():
    with st.sidebar:
        
        social_media_html = """
            <div style="text-align: center;">
                <h2>Redes Sociais</h2>
                <a href="https://www.instagram.com/falkzera/" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" style="width:40px;height:40px;margin:10px;">
                </a>
                <a href="https://github.com/falkzera" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" style="width:40px;height:40px;margin:10px;">
                </a>
                <a href="https://www.linkedin.com/in/falkzera/" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" style="width:40px;height:40px;margin:10px;">
                </a>
                <a href="https://medium.com/@falkzera" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/Medium_logo_Monogram.svg" alt="Medium" style="width:40px;height:40px;margin:10px;">
                </a>
                <p style="text-align: center;">Developer by: <a href="https://GitHub.com/Falkzera" target="_blank">Lucas Falcão</a></p>
            </div>
            """
        st.markdown(social_media_html, unsafe_allow_html=True)

if __name__ == "__main__":
    display_credits()