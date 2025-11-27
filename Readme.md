# Data Cleaning & Quality Checker

A comprehensive web application for analyzing, cleaning, and reporting on data quality issues in datasets. Built with Streamlit, this tool provides interactive data quality analysis, intelligent cleaning recommendations, and export capabilities.

## ✨ Features

- **Data Quality Analysis**
  - Detects missing values with percentages
  - Identifies outliers using IQR method
  - Finds categorical inconsistencies (case, whitespace issues)
  - Reports duplicate rows
  - Shows data types for each column

- **Intelligent Recommendations**
  - Suggests appropriate handling for missing values based on percentage
  - Recommends outlier treatment methods
  - Identifies text standardization needs
  - Provides column removal suggestions

- **Interactive Cleaning Operations**
  - Fill missing values (mean, median, mode)
  - Handle outliers (capping, removal)
  - Standardize text values (trim whitespace, normalize case)
  - Remove columns or duplicate rows
  - Apply transformations through a user-friendly form

- **Export Capabilities**
  - Download cleaned dataset in CSV format
  - Generate detailed cleaning report
  - Track all applied transformations

## 🛠️ Requirements

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Scipy
- Scikit-learn
- Matplotlib
- Seaborn

## 🚀 Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd data-cleaning-app
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📋 Usage

1. **Upload Data**: Use the file uploader to load your CSV or Excel file
2. **Analyze Data**: Click "Run Data Quality Analysis" to get insights
3. **Review Recommendations**: Check the suggested cleaning actions
4. **Apply Transformations**: Use the form to select and apply cleaning operations
5. **Export Results**: Download the cleaned dataset and report

## 🏗️ Architecture

The application is built with:
- **Streamlit** for the web interface
- **Pandas** for data manipulation
- **NumPy** for numerical operations
- **Scikit-learn** for preprocessing
- **SciPy** for statistical operations
- **Matplotlib/Seaborn** for visualizations

## 📁 File Structure

```
├── app.py              # Main Streamlit application
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## 📊 Supported Data Types

- Numerical columns (int, float)
- Categorical columns (object/string)
- Date columns (when properly formatted)
- Mixed-type columns

## ⚙️ Configuration

The application uses Streamlit's session state to maintain data across interactions. No additional configuration is needed for basic operation.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the repository with:
- Python version
- Error message
- Steps to reproduce
- Expected behavior

<img width="1738" height="815" alt="image" src="https://github.com/user-attachments/assets/b1af561b-bc7b-46d8-a748-76fc1ddf6635" />

<img width="1724" height="647" alt="image" src="https://github.com/user-attachments/assets/b44ac9a8-d3fd-463e-8cc7-a1243a0c979d" />


<img width="1684" height="518" alt="image" src="https://github.com/user-attachments/assets/fbebb8a3-7420-4590-b8cf-6f7a46cd904b" />


<img width="540" height="421" alt="image" src="https://github.com/user-attachments/assets/5a1fe533-95ec-4fa1-a0dd-fe8da07f9a4f" />

<img width="1677" height="815" alt="image" src="https://github.com/user-attachments/assets/77853eeb-4a97-4278-b5bb-890ef2c26f84" />

<img width="1711" height="675" alt="image" src="https://github.com/user-attachments/assets/7177dfa0-784f-4910-884e-b2337bc4a88b" />


