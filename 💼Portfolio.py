# import the Streamlit library
import streamlit as st
from PIL import Image  # PIL 모듈 추가

# Configure page settings
st.set_page_config(
    page_title='Template',
    layout="wide",
    initial_sidebar_state="auto",
    page_icon='👧🏻'
)

# Load local CSS styles
def local_css(file_name):
    with open(file_name, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles/styles_main.css")

# Define variables (assuming 'info' and 'projects' are defined somewhere)
info = {
    'Pronoun': 'your',  # Sample data, replace with actual values
    'Full_Name': 'Your Name',  # Sample data, replace with actual values
    'Intro': 'Intro text',  # Sample data, replace with actual values
    'About': 'About text',  # Sample data, replace with actual values
    'Email': 'your-email@example.com',  # Sample data, replace with actual values
    'Project': 'https://example.com/projects',  # Sample data, replace with actual values
    'Medium': 'https://example.com/medium',  # Sample data, replace with actual values
}

projects = [
    {
        'title': 'Project 1',
        'description': 'Description of Project 1',
        'image_url': 'https://example.com/image1.jpg',
        'link': 'https://example.com/project1',
    },
    {
        'title': 'Project 2',
        'description': 'Description of Project 2',
        'image_url': 'https://example.com/image2.jpg',
        'link': 'https://example.com/project2',
    },
    {
        'title': 'Project 3',
        'description': 'Description of Project 3',
        'image_url': 'https://example.com/image3.jpg',
        'link': 'https://example.com/project3',
    },
]

# App sidebar
with st.sidebar:
    st.markdown("# Chat with my AI assistant")

    with st.expander("Click here to see FAQs"):
        st.info(
            """
            - What are your strengths and weaknesses?
            - What is your expected salary?
            - What is your latest project?
            - When can you start to work?
            - Tell me about your professional background
            - What is your skillset?
            - What is your contact?
            - What are your achievements?
            """
        )

    st.caption("© Made by Vicky Kuo 2023. All rights reserved.")

# Main content
with st.container():
    col1, col2 = st.columns([8, 3])

    # Column 1
    with col1:
        st.markdown(f"## Hi, I'm {info['Full_Name']} 👋")
        st.write("")
        st.write(info['About'])

        # Buttons to switch pages
        with st.columns([0.35, 0.2, 0.45]):
            if st.button("Chat with My AI Assistant"):
                st.experimental_set_query_params(page="AI_Assistant_Chat")

            if st.button("My Resume"):
                st.experimental_set_query_params(page="Resume")

    # Column 2
    with col2:
        profile = Image.open("images/profile.png")
        st.image(profile, width=280)

# Additional sections
with st.container():
    st.write("---")
    st.subheader('🚀 Project Showcase')

    columns = st.columns(3)
    for i, project in enumerate(projects):
        with columns[i % 3]:
            st.markdown(f'<a href="{project["link"]}" target="_blank">'
                        f'<img src="{project["image_url"]}" style="width:100%;height:auto;"></a>',
                        unsafe_allow_html=True)
            st.markdown(f'**{project["title"]}**<br>{project["description"]}', unsafe_allow_html=True)

    st.markdown(f'<a href="{info["Project"]}">👀 Click here to see more</a>', unsafe_allow_html=True)

with st.container():
    st.write("---")
    st.subheader('✍️ Medium')

    col1, col2 = st.columns([0.95, 0.05])
    components.html(
        """
        <style>
            .rss-content {
                height: 300px;
                overflow-y: auto;
            }
        </style>
        """,
        height=0,
        width=0,
    )
    st.markdown(f'<a href="{info["Medium"]}">👀 Click here to see more</a>', unsafe_allow_html=True)

st.write("---")
with st.container():
    col1, col2, col3 = st.columns([0.475, 0.475, 0.05])

    with col1:
        st.subheader("👄 Coworker Endorsements")
        st.html(
            """
            <div class="slideshow-container">
                <div class="mySlides fade">
                    <img src="{endorsements['img1']}" style="width:100%">
                </div>
                <div class="mySlides fade">
                    <img src="{endorsements['img2']}" style="width:100%">
                </div>
                <div class="mySlides fade">
                    <img src="{endorsements['img3']}" style="width:100%">
                </div>
            </div>

            <br>
            <div style="text-align:center">
                <span class="dot"></span> 
                <span class="dot"></span> 
                <span class="dot"></span> 
            </div>

            <script>
                let slideIndex = 0;
                showSlides();

                function showSlides() {{
                    let i;
                    let slides = document.getElementsByClassName("mySlides");
                    let dots = document.getElementsByClassName("dot");
                    for (i = 0; i < slides.length; i++) {{
                        slides[i].style.display = "none";  
                    }}
                    slideIndex++;
                    if (slideIndex > slides.length) {{slideIndex = 1}}    
                    for (i = 0; i < dots.length; i++) {{
                        dots[i].className = dots[i].className.replace(" active", "");
                    }}
                    slides[slideIndex - 1].style.display = "block";  
                    dots[slideIndex - 1].className += " active";
                    setTimeout(showSlides, 2500); // Change image every 2.5 seconds
                }}

                // Pause/resume slideshow on hover
                function pauseSlides() {{
                    clearInterval(interval);
                }}

                function resumeSlides() {{
                    interval = setInterval(showSlides, 2500);
                }}

                let interval = setInterval(showSlides, 2500);

                // Set up event listeners for the slides
                let slides = document.getElementsByClassName("mySlides");
                for (let i = 0; i < slides.length; i++) {{
                    slides[i].addEventListener("mouseover", pauseSlides);
                    slides[i].addEventListener("mouseout", resumeSlides);
                }}
            </script>
            """,
            height=270,
        )

    with col2:
        st.subheader("📨 Contact Me")
        email = info["Email"]
        contact_form = f"""
        <form action="https://formsubmit.co/{email}" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)

# JavaScript to change button color
def change_button_color(widget_label, background_color='transparent'):
    html_str = f"""
        <script>
            let buttons = document.querySelectorAll('button');
            buttons.forEach(button => {{
                if (button.innerText === '{widget_label}') {{
                    button.style.background = '{background_color}';
                }}
            }});
        </script>
    """
    st.components.v1.html(html_str, height=0)

change_button_color('Chat with My AI Assistant', '#0cc789')
