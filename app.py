import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Mathematical Analysis Topology Analyzer", layout="wide")

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main { background-color: #f7f9fc; }
h1, h2, h3 { color: #1f4e79; }
.stButton > button { border-radius: 10px; }
.block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("Mathematical Analysis Topology Analyzer")
st.write("""
Analyze **open/closed sets**, **closure**, **boundary**, **limit points**,
visualize **open balls**, simulate **sequence convergence**,
explore **epsilon-delta**, and advanced topology properties.
""")

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.header("Settings")
metric_mode = st.sidebar.selectbox("Choose Metric", [
    "Euclidean", "Discrete", "Manhattan (Taxicab)",
    "Squared Euclidean", "Maximum / Chebyshev",
    "Cubic Metric", "Weighted Euclidean", "Custom Formula"
])
custom_metric = ""
if metric_mode == "Custom Formula":
    custom_metric = st.sidebar.text_input("Enter d(x,y):", value="abs(x-y)")

center = st.sidebar.number_input("Ball Center", value=0.0)
radius = st.sidebar.number_input("Ball Radius", min_value=0.1, value=0.5)

# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Topology & Sets",
    "Sequence Convergence",
    "Epsilon-Delta",
    "Advanced Analysis"
])

# =====================================================
# TAB 1: Topology & Sets
# =====================================================
with tab1:
    st.header("Topology and Set Analysis")
    set_mode = st.selectbox("Choose a predefined set or custom", [
        "(0,1)", "[0,1]", "(0,∞)", "(-∞,0)",
        "ℕ (Natural Numbers)", "ℤ (Integers)",
        "ℚ (Rational Numbers)", "ℝ (Real Numbers)",
        "ℝ \\ ℚ (Irrational Numbers)", "Cantor Set",
        "Finite Set {1,2,3}", "Singleton {0}", "Custom Set"
    ])
    if set_mode == "Custom Set":
        user_set = st.text_input("Enter your custom set:", value="(0,1)")
    else:
        user_set = set_mode

    st.write(f"### Analysis of: `{user_set}`")

    # Symbolic set analysis
    analysis_text = []
    if user_set == "(0,1)":
        analysis_text = ["Open: Yes", "Closed: No", "Closure: [0,1]", "Boundary: {0,1}", "Limit points: [0,1]", "Convex: Yes", "Compact: No", "Connected: Yes"]
    elif user_set == "[0,1]":
        analysis_text = ["Open: No", "Closed: Yes", "Closure: [0,1]", "Boundary: {0,1}", "Limit points: [0,1]", "Convex: Yes", "Compact: Yes", "Connected: Yes"]
    elif "Rational" in user_set:
        analysis_text = ["Open: No", "Closed: No", "Dense in ℝ", "Closure: ℝ", "Every real number is a limit point", "Connected: No"]
    elif "Cantor" in user_set:
        analysis_text = ["Closed: Yes", "Perfect", "Totally disconnected", "Compact: Yes"]
    else:
        analysis_text = ["Custom symbolic analysis not implemented."]

    for line in analysis_text:
        st.write(f"- {line}")

    # Interior / Closure / Boundary Visualizer
    st.subheader("Interior / Closure / Boundary Visualizer")
    fig_vis = plt.figure(figsize=(8, 1.8))
    ax_vis = fig_vis.add_subplot(111)
    ax_vis.axhline(0, color='black')
    ax_vis.set_ylim(-1, 1)
    ax_vis.set_yticks([])
    if user_set in ["(0,1)", "[0,1]"]:
        ax_vis.plot([0,1],[0,0], linewidth=10, alpha=0.3)  # closure
        ax_vis.scatter([0,1],[0,0], s=80)  # boundary
    st.pyplot(fig_vis)

    # Limit Point Explorer
    st.subheader("Limit Point Explorer")
    point = st.number_input("Enter a point to test", value=0.0)
    if user_set == "(0,1)":
        if 0 <= point <= 1:
            st.success("This is a limit point.")
        else:
            st.warning("Not a limit point.")

    # Open Ball Visualization
    st.subheader("Open Ball Visualization")
    fig = plt.figure(figsize=(8, 2))
    ax = fig.add_subplot(111)
    ax.axhline(0, color='black')
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    x = np.linspace(center - 2, center + 2, 500)

    if metric_mode == "Euclidean":
        inside = np.abs(x - center) < radius
    elif metric_mode == "Discrete":
        inside = np.ones_like(x, dtype=bool) if radius > 1 else np.isclose(x, center)
    elif metric_mode == "Manhattan (Taxicab)":
        inside = np.abs(x - center) < radius
    elif metric_mode == "Squared Euclidean":
        inside = (x - center)**2 < radius
    elif metric_mode == "Maximum / Chebyshev":
        inside = np.maximum(np.abs(x-center),0) < radius
    elif metric_mode == "Cubic Metric":
        inside = np.abs((x-center)**3) < radius
    elif metric_mode == "Weighted Euclidean":
        inside = 2*np.abs(x-center) < radius
    else:
        vals=[]
        for p in x:
            try:
                vals.append(eval(custom_metric,{"x":p,"y":center,"abs":abs,"np":np})<radius)
            except:
                vals.append(False)
        inside = np.array(vals)

    ax.scatter(x[inside], np.zeros_like(x[inside]), s=8)
    ax.plot(center,0,'o')
    ax.set_title(f"Open Ball under {metric_mode}")
    st.pyplot(fig)

# =====================================================
# TAB 2: Sequences
# =====================================================
with tab2:
    st.header("Sequence Convergence Simulator")
    sequence_mode = st.selectbox("Choose Sequence", ["1/n", "(-1)^n", "n/(n+1)", "Custom"])
    custom_seq = ""
    if sequence_mode == "Custom":
        custom_seq = st.text_input("Enter a_n in terms of n:", value="1/n")
    n = np.arange(1,30)

    if sequence_mode == "1/n":
        vals = 1/n
        st.success("Converges to 0 | Cauchy: Yes")
    elif sequence_mode == "(-1)^n":
        vals = (-1)**n
        st.warning("Divergent | Cauchy: No")
    elif sequence_mode == "n/(n+1)":
        vals = n/(n+1)
        st.success("Converges to 1 | Cauchy: Yes")
    else:
        try:
            vals = eval(custom_seq,{"n":n,"np":np})
            st.info("Custom sequence plotted.")
        except:
            vals = np.zeros_like(n)
            st.error("Invalid formula.")

    fig2 = plt.figure(figsize=(8,3))
    plt.plot(n, vals, 'o-')
    plt.title("Sequence Plot")
    plt.xlabel("n")
    plt.ylabel("a_n")
    st.pyplot(fig2)

# =====================================================
# TAB 3: Epsilon-Delta
# =====================================================
with tab3:
    st.header("Epsilon-Delta Visualization")
    epsilon = st.slider("ε (epsilon)", 0.1, 2.0, 0.5)
    delta = st.slider("δ (delta)", 0.1, 2.0, 0.7)
    st.write("Example function: f(x)=x² at x=1")
    x = np.linspace(0,2,300)
    y = x**2
    fig3 = plt.figure(figsize=(8,4))
    plt.plot(x,y)
    plt.axvspan(1-delta,1+delta,alpha=0.2)
    plt.axhspan(1-epsilon,1+epsilon,alpha=0.2)
    plt.title("Epsilon-Delta Neighborhood")
    st.pyplot(fig3)

# =====================================================
# TAB 4: Advanced Analysis
# =====================================================
with tab4:
    st.header("Advanced Analysis")

    # Metric Equivalence Checker
    st.subheader("Metric Equivalence Checker")
    m1 = st.selectbox("Metric 1", ["Euclidean", "Manhattan", "Discrete"])
    m2 = st.selectbox("Metric 2", ["Euclidean", "Manhattan", "Discrete"])
    if (m1,m2) in [("Euclidean","Manhattan"),("Manhattan","Euclidean")]:
        st.success("Equivalent on ℝ")
    elif m1 == m2:
        st.success("Equivalent (same metric)")
    else:
        st.warning("Not equivalent")

    # PDF Export
    st.subheader("Generate PDF Report")
    if st.button("Generate PDF"):
        filename = "analysis_report.pdf"
        doc = SimpleDocTemplate(filename)
        styles = getSampleStyleSheet()
        story = [Paragraph("Mathematical Analysis Report", styles['Title']), Spacer(1,12)]
        for line in analysis_text:
            story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1,6))
        doc.build(story)
        with open(filename, "rb") as f:
            st.download_button("Download PDF", f, file_name=filename)

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.write("Created By:")
st.write("Meysam Mohseny")
