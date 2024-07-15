import logging
import streamlit as st  # type: ignore
from bug_report_generator import check_api_key, process_user_input

# Configure logging (optional, adjust log level and output as needed)
logging.basicConfig(level=logging.INFO,
					format='%(asctime)s - %(levelname)s - %(message)s')


def get_user_steps():
	return st.text_area("How do you reproduce the bug? 🐞",
						placeholder="e.g.\nClick login, fill email & OTP,  click submit, \"Failed to Login\"",
						value="",
						height=150)


def get_expected_results():
	return st.text_area("What do you expect to see? 👀",
						placeholder="e.g.\nRedirect to homepage",
						value="",
						height=150)


def get_test_env():
	return st.text_area("Test environment details",
						placeholder="",
						value="- Environment: UAT\n- Platform: \n- Build version: \n- Browser: \n- Device (OS version): \n- Test account:",
						height=170,
						help="This helps in issue replication and investigation.")


def show_caption_before():
	caption = f"Streamline your QA process with ease!\n\n"
	caption += f"👈🏻 Input your bug details, and let our AI generate clear and consistent bug reports for you."
	st.write(caption)


def show_caption_after():
	caption = f"Report generated 🎉\n\n"
	caption += f"*💡 If the result is not accurate, try to refine your input with more information.*"
	st.write(caption)


def show_placeholder(message="Loading..."):
	custom_container = """
			<div class="pre-generate-container">
				<div class="pre-generate-icon">
					<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="pre-generate-icon-svg">
						<rect width="24" height="24" fill="none"></rect>
						<path d="M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3zm-2 10H6V7h12v12zm-9-6c-.83 0-1.5-.67-1.5-1.5S8.17 10 9 10s1.5.67 1.5 1.5S9.83 13 9 13zm7.5-1.5c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5.67-1.5 1.5-1.5 1.5.67 1.5 1.5zM8 15h8v2H8v-2z"></path>
					</svg>
				</div>
				<div class="pre-generate-message">{}</div>
			</div>
			""".format(message)

	with st.container(height=160, border=True):
		st.markdown(custom_container, unsafe_allow_html=True)


try:
	# Check if required API key exists
	check_api_key()

	# Streamlit App Interface
	st.set_page_config(
		page_title="IssueSnap",
		page_icon="⚡️",
		layout="centered",
		initial_sidebar_state="expanded",
		menu_items=None
	)

	# Custom CSS for centering the text and changing the font
	st.markdown(
		"""
				<style>
				.pre-generate-container {
					height: 130px;
					display: flex;
					align-items: center;
					justify-content: center;
					gap: 0.5rem;
				}
				.pre-generate-icon {
					display: flex;
					width: 2rem;
					height: 2rem;
					flex-shrink: 0;
					border-radius: 0.5rem;
					-webkit-box-align: center;
					align-items: center;
					-webkit-box-pack: center;
					justify-content: center;
					background-color: rgb(255, 189, 69);
				}
				.pre-generate-icon-svg {
					vertical-align: middle;
					overflow: hidden;
					color: inherit;
					fill: currentcolor;
					display: inline-flex;
					-webkit-box-align: center;
					align-items: center;
					font-size: 1.25rem;
					width: 1.25rem;
					height: 1.25rem;
					flex-shrink: 0;
				}
				.pre-generate-message {
					font-family: Source Code Pro;
					font-style: italic;
					font-size: 16px;
				}
	
				a:link , a:visited{
					color: inherit;
					background-color: transparent;
					text-decoration: none;
				}

				a:hover,  a:active {
					color: inherit;
					background-color: transparent;
					text-decoration: none;
				}
				</style>
				""",
		unsafe_allow_html=True
	)

	# Sidebar input view
	with st.sidebar:
		st.header("👇🏻 Tell me your bug")
		user_steps = get_user_steps()
		expected_results = get_expected_results()
		test_env = get_test_env()
		gen_btn = st.button("Generate", type="primary",
							use_container_width=True)
		st.caption("[Made with Passion © OURSKY](%s)" %
				   "https://www.oursky.com")

	# Main view
	st.title("IssueSnap")
	loading_holder = st.empty()
	result_holder = st.empty()
	if gen_btn:
		# Show loading in container
		with loading_holder.container():
			result_holder.empty()
			show_caption_before()
			show_placeholder("Generating...")
			response = process_user_input(
				user_steps, expected_results, test_env)
		# Show results in container
		if response:
			with result_holder.container():
				loading_holder.empty()
				show_caption_after()
				with st.container(border=True):
					st.write(response)
				st.write("Happy Testing!🌟")
	else:
		with result_holder.container():
			# Show default placeholder in container
			show_caption_before()
			show_placeholder("Your bug report will be generated here")


except KeyError as e:
	st.error(f"Missing environment variable: {e}")
	logging.error(f"chatbot.py: Missing environment variable: {e}")
except Exception as e:
	st.error(f"Uh oh! We seem to be having a hiccup. Give it another shot soon?")
	logging.error(f"chatbot.py: Exception: {e}")
