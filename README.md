# 🏏 IPL Win Probability Predictor

An interactive, machine-learning-powered web application that estimates the win probability of chasing teams in Indian Premier League (IPL) matches in real-time.

**Developed by:** **Aditya Kumar** 👨‍💻

---

## 🌟 Key Features
- **Modern Glassmorphism UI/UX**: Frosted glass effects, responsive cards, neon gradients, and polished typography.
- **Dynamic In-Game Analytics**: Calculates Current Run Rate (CRR), Required Run Rate (RRR), Runs Needed, and Balls Remaining automatically.
- **Machine Learning Pipeline**: Trained on ball-by-ball IPL match data with `scikit-learn` (ColumnTransformer + Logistic Regression).
- **Edge-Case Handled**: Handles boundary cases (overs completion, target achieved, all out, over fractions, etc.).
- **Streamlit Cloud Ready**: Clean UTF-8 dependencies, cached resource loading, and production configuration.

---

## 🚀 Live Demo & Deployment
This application is configured for one-click deployment on **[Streamlit Community Cloud](https://streamlit.io/cloud)**.

### How to Run Locally:
1. Clone the repository:
   ```bash
   git clone https://github.com/adityaX11/machin_learning.git
   cd machin_learning
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```

---

## 🛠️ Tech Stack
- **Frontend**: Streamlit, Custom Glassmorphism CSS (HTML5/CSS3)
- **Machine Learning**: Scikit-Learn, Pandas, NumPy
- **Deployment**: Streamlit Cloud

---

## 👨‍💻 Author
**Aditya Kumar**  
- GitHub: [@adityaX11](https://github.com/adityaX11)
