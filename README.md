# City Helper Bot 🚦🌦️

A Telegram-based virtual assistant designed to provide real-time information on weather and traffic. This project leverages the power of **Azure** to ensure scalability, monitoring, and security.


## 🌟 **Project Goal**

Create a simple and intuitive urban assistance system that allows users to access useful information through Telegram commands, utilizing a serverless infrastructure on Azure.

## 🚀 **Main Features**

1. **Weather Forecast**:  
   - Command: `/meteo [city]`  
   - Example: `/meteo Roma`  
   - Provides detailed weather forecasts for the specified city.

2. **Real-Time Traffic Monitoring**:  
   - Command: `/traffico [city]`  
   - Example: `/traffico Milano`  
   - Returns real-time updates on urban traffic conditions.

3. **Credit Management**:  
   - **Add credits**: `/ricarica` (adds 5 credits).  
   - **Credit consumption**: each `/meteo` and `/traffico` command reduces credits by 1.  
   - Credit balance included in the responses.

4. **Authentication via Azure Entra ID**:  
   - Authentication and registration are managed through a custom flow in Azure Entra ID.
   - Unauthenticated users are redirected to a custom link generated and managed by Azure Entra ID to complete the authentication/registration process.
   - Once authenticated, users can access all bot features seamlessly.

5. **Request Tracking**:  
   - Detailed logs for user, date, and request type.  
   - Error and anomaly monitoring through **Azure Monitor** and **Application Insights**.

## 🛠️ **Architectural Components**

### **1. Frontend - Telegram Bot**
- Direct interaction with the user via commands.
- Use of custom webhooks to handle communication with the backend on **Azure**.

### **2. Serverless Processing on Azure**
- **Azure Functions**:
  - Handling business logic.
  - Processing requests and interacting with external APIs.
- **Serverless Architecture**: dynamic scalability to optimize costs.

### **3. Authentication with Azure Entra ID**
- The bot provides a login link to unauthenticated users.
- If the user is not registered, Azure Entra ID automatically completes the registration during the login process.
- This ensures a seamless experience, requiring only a single interaction with the login link.

### **4. Database - Azure Cosmos**
- Storing Telegram users and their credits.
- User identification via Telegram ID.

### **5. Monitoring and Security**
- Request tracking and error handling through:
  - **Azure Monitor**
  - **Application Insights**
- Secure handling of sensitive data via **Azure Key Vault**.

## 📦 **Requirements**

### **1. Python Dependencies**
Make sure to install the dependencies specified in `requirements.txt`:

```plaintext
azure-functions==1.21.3
azure-identity==1.19.0
azure-keyvault-secrets==4.9.0
azure-cosmos==4.9.0
azure-monitor-opentelemetry==1.6.4
opencensus-ext-azure==1.1.13
opentelemetry-sdk==1.28.2
python-telegram-bot==20.7
aiohttp==3.9.1
requests==2.31.0
python-dotenv==1.0.0
```

Install the dependencies with:
```bash
pip install -r requirements.txt
```

### **2. Environment Configuration**
Create a `.env` file and configure the following variables:
```plaintext
TELEGRAM-BOT-TOKEN=
TELEGRAM-SECRET-TOKEN=
AZURE-KEY-VAULT-NAME=
APPLICATIONINSIGHTS_CONNECTION_STRING=
INSTRUMENTATION-KEY=
COSMOS-DB-URL=
COSMOS-DB-KEY=
OPENWEATHER-API-KEY=
TRAFFIC-API-KEY=
AZURE-TENANT-ID=
AZURE-CLIENT-ID=
AZURE-CLIENT-SECRET=
SUBSCRIPTION-API-KEY=
```

## 🧑‍💻 **Available Telegram Commands**

| Command           | Description                                      | Credits Consumed  |
|-------------------|--------------------------------------------------|-------------------|
| `/meteo [city]`   | Provides the weather forecast for the city.      | 1                 |
| `/traffico [city]`| Shows real-time traffic updates for the city.    | 1                 |
| `/ricarica`       | Adds 5 credits to your account.                  | 0                 |

## 📊 **Monitoring**

- **Azure Monitor**: Tracking requests to the bot.
- **Application Insights**: Logging errors and anomalies.

## 📂 **Project Structure**

```plaintext
city-helper-bot/
├── auth/                      # Modules for authentication
├── commands/                  # Modules for handling specific commands
├── services/                  # Modules for integrating with APIs and databases
├── utils/                     # General helpers (e.g., logging, metrics)
├── .env.example               # Example configuration file
├── function_app.py            # Entry point of the application
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## 📖 **How to Run**

1. Clone the repository:
   ```bash
   git clone https://github.com/iamcarminecristian/city-helper-bot.git
   cd CityHelperCCBot
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the `.env` file as described.

4. Run the application locally:
   ```bash
   func start
   ```

5. Register the webhook for your Telegram bot by running:
   ```bash
   curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook?url=<AZURE_FUNCTION_URL>
   ```

## 🛡️ **Security**

- Credentials are stored in **Azure Key Vault**.
- Authentication is handled via **Azure Entra ID**.
- Request and error tracking are active via **Azure Monitor**.

## 🤝 **Contributions**

We welcome contributions! Feel free to submit a pull request or open an issue to report bugs or suggest new features.
