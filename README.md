# Morphological Time Series Engine

Applies mathematical morphology operators (erosion, dilation, opening, closing) to ETF price series. Extracts trend (opening) and anomaly (residual) components. The score can be the slope of the morphological trend or the negative standard deviation of residuals. Higher score indicates stronger upward trend or lower anomaly → overweight signal.

- **Morphological operators:** flat/linear structuring element
- **Score types:** trend_slope or anomaly_std (inverted)
- **Windows:** 63, 252, 504, 1008, 2016 days (best per ETF)
- **Output:** top 3 ETFs per universe

Runs daily on GitHub Actions.

## Local execution

```bash
pip install -r requirements.txt
export HF_TOKEN=<your_token>
python trainer.py
streamlit run streamlit_app.py
