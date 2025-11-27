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
