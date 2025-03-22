

# Founder-Investor Matching Notebook

This Jupyter Notebook implements an AI-powered founder-investor matching system using Google Gemini AI. It allows users to select a sample founder profile and match it against a predefined set of investor profiles to find compatible investors based on industry, stage, funding requirements, and other criteria.

## Features
- **Founder Profiles**: Choose from a predefined list of sample founder profiles with details like startup name, industry, stage, funding required, traction, and business model.
- **Investor Data**: Uses a hardcoded list of sample investor profiles with details like name, industry preferences, investment range, and preferred stages.
- **Compatibility Analysis**: Leverages Google Gemini AI to evaluate compatibility and return a match score and reasoning.
- **Output**: Displays matches in the notebook and saves results to a text file.

## Prerequisites
- **Python 3.8+**: Ensure Python is installed on your system.
- **Jupyter Notebook**: Required to run the notebook interactively.
- **Google Gemini API Key**: You need a valid API key from Google Gemini to use the AI model.

## Installation
1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
   Alternatively, download the `.ipynb` file manually.

2. **Install Dependencies**:
   Install the required Python packages using pip:
   ```bash
   pip install google-generativeai
   ```
   - `google-generativeai`: For accessing the Gemini AI model.
   - Other dependencies (`json`, `re`) are part of the Python standard library.

3. **Set Up API Key**:
   Replace the placeholder API key in Cell 2 with your actual Google Gemini API key:
   ```python
   genai.configure(api_key="YOUR_ACTUAL_API_KEY_HERE")
   ```

## Usage
1. **Open the Notebook**:
   Launch Jupyter Notebook and open the `.ipynb` file:
   ```bash
   jupyter notebook
   ```

2. **Run Cells Sequentially**:
   The notebook is divided into 9 cells. Execute them in order:
   - **Cell 1**: Imports required libraries.
   - **Cell 2**: Configures the Gemini API and initializes variables.
   - **Cell 3**: Defines the `analyze_compatibility_gemini` function for AI analysis.
   - **Cell 4**: Defines the `calculate_matches` function for matching logic.
   - **Cell 5**: Loads sample investor data into `INVESTOR_DATA`.
   - **Cell 6**: Allows selection of a sample founder profile.
   - **Cell 7**: Calculates and displays matches.
   - **Cell 8**: Saves match results to a text file.
   - **Cell 9**: Prints footer information.

3. **Select Founder Profile**:
   In Cell 6, enter a number (0-7) to choose a sample founder profile when prompted.

4. **View Results**:
   - Matches are printed in Cell 7 with investor names, scores, and reasoning.
   - A text file with results is saved in the working directory (Cell 8).

## Sample Data

### Sample Founder Profiles (Cell 6)
| Index | Name                  | Industry     | Stage     | Funding Required | Traction         | Business Model |
|-------|-----------------------|--------------|-----------|------------------|------------------|----------------|
| 0     | BlastApp             | Fintech      | Seed      | $500,000         | 20K users        | SaaS           |
| 1     | HealthTech Innovate  | Healthcare   | Series A  | $2,000,000       | $500K revenue    | B2B            |
| 2     | Web3 Pioneer         | Web3         | Pre-Seed  | $12,000          | 1K beta users    | Subscription   |
| 3     | EcoSolutions         | Energy       | Series+   | $5,000,000       | $3M revenue      | B2C            |
| 4     | IoT Connect          | IoT          | Seed      | $100,000         | 10K devices sold | Hardware       |
| 5     | EduPlatform          | Edtech       | Pre-Seed  | $200,000         | 5K students      | SaaS           |
| 6     | MarketMate           | Marketplace  | Series A  | $2,000,000       | $1M GMV          | B2C            |
| 7     | MediTech Solutions   | Medtech      | Series+   | $8,000,000       | $4M revenue      | B2B            |

### Sample Investor Profiles (Cell 5)
| Name                   | Industry                              | Stage                      | Cheque Range    |
|-----------------------|---------------------------------------|----------------------------|-----------------|
| Blast.Club            | IoT, SaaS, Consumer, Edtech, Fintech  | Pre-seed, Seed, Series+    | $500K - $5M     |
| Blisce/               | B2C                                   | Pre-seed, Series A         | $10M - $20M     |
| Block Dojo            | Web3                                  | Pre-seed, Idea, Prototype  | $12K - $12K     |
| Blockchain Founders   | Sector Agnostic (Web3 focus)          | Pre-seed, Seed, Series+    | $200K - $1M     |
| Blockrocket           | Sector Agnostic (Blockchain focus)    | Pre-seed, Seed             | $100K - $500K   |
| Blue Collective       | Sector Agnostic                       | Pre-seed, Seed, Series+    | $200K - $2M     |
| Blue Future Partners  | SaaS                                  | Pre-seed, Series+          | $2M - $5M       |
| Blue Heron Capital    | IT & Services                         | Pre-seed, Seed, Series+    | $2M - $8M       |

## Example Workflow
1. Run Cells 1-5 to set up the environment and load investor data.
2. In Cell 6, enter `2` to select "Web3 Pioneer".
3. Run Cell 7 to see matches (e.g., "Block Dojo" might match due to Web3 focus).
4. Run Cell 8 to save results to `Web3_Pioneer_investor_matches.txt`.
5. Run Cell 9 for footer info.

## Troubleshooting
- **API Key Error**: Ensure your Gemini API key is valid and correctly inserted.
- **No Matches**: Check if `INVESTOR_DATA` is loaded (Cell 5) and if the founder profile aligns with investor preferences.
- **Module Not Found**: Install `google-generativeai` if you see import errors.

## Limitations
- **Static Data**: Investor data is hardcoded; modify Cell 5 to load from a JSON file if needed.
- **No UI**: This is a command-line-style notebook without interactive widgets.
- **API Dependency**: Requires an active internet connection and Gemini API access.

## Contributing
Feel free to fork this project, add more sample data, or enhance functionality (e.g., file-based investor loading). Submit pull requests or open issues for suggestions.

## Credits
- **Powered by**: Google Gemini AI
- **Developed by**: Amresh Yadav
- **Contact**: maithilgeek@gmail.com, +91-7260905948




