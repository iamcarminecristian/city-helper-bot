# Urban Assistance Bot 🚦🌦️

A Telegram-based virtual assistant designed to provide real-time information on weather and traffic. This project leverages the power of **Azure** to ensure scalability, monitoring, and security.


## 🌟 **Project Goal**

Create a simple and intuitive urban assistance system that allows users to access useful information through Telegram commands, utilizing a serverless infrastructure on Azure.

## 🚀 **Main Features**

1. **Weather Forecast**:  
   - Command: `/weather [city]`  
   - Example: `/weather Rome`  
   - Provides detailed weather forecasts for the specified city.

2. **Real-Time Traffic Monitoring**:  
   - Command: `/traffic [city]`  
   - Example: `/traffic Milan`  
   - Returns real-time updates on urban traffic conditions.

3. **Credit Management**:  
   - **Add credits**: `/recharge` (adds 20 credits).  
   - **Credit consumption**: each `/weather` and `/traffic` command reduces credits by 1.  
   - Credit balance included in the responses.

4. **Request Tracking**:  
   - Detailed logs for user, date, and request type.  
   - Error and anomaly monitoring through **Azure Monitor** and **Application Insights**.

5. **Integration with External APIs**:  
   - Collection and standardization of data from weather and traffic services.

## 🛠️ **Architectural Components**

### **1. Frontend - Telegram Bot**
- Direct interaction with the user via commands.
- Use of custom webhooks to handle communication with the backend on **Azure**.

### **2. Serverless Processing on Azure**
- **Azure Functions**:
  - Handling business logic.
  - Processing requests and interacting with external APIs.
- **Serverless Architecture**: dynamic scalability to optimize costs.

### **3. Database - Azure Cosmos**
- Storing Telegram users and their credits.
- User identification via Telegram ID.

### **4. Monitoring and Security**
- Request tracking and error handling through:
  - **Azure Monitor**
  - **Application Insights**

## 📦 **Requirements**

### **1. Python Dependencies**
Make sure to install the dependencies specified in `requirements.txt`:

```plaintext
azure-functions==1.14.0
azure-identity==1.13.0
azure-keyvault-secrets==4.8.0
azure-cosmos==4.3.0
azure-monitor-opentelemetry==1.0.0b15
opencensus-ext-azure==1.1.8
opentelemetry-sdk==1.19.0
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
```

## 🧑‍💻 **Available Telegram Commands**

| Command           | Description                                      | Credits Consumed |
|-------------------|--------------------------------------------------|-------------------|
| `/meteo [city]`  | Provides the weather forecast for the city.     | 1                 |
| `/traffico [city]`  | Shows real-time traffic updates for the city.   | 1                 |
| `/ricarica`        | Adds 20 credits to your account.                | 0                 |

## 📊 **Monitoring**

- **Azure Monitor**: Tracking requests to the bot.
- **Application Insights**: Logging errors and anomalies.

## 📂 **Project Structure**

```plaintext
city-helper-bot/
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
- Request and error tracking are active via **Azure Monitor**.

## 🤝 **Contributions**

We welcome contributions! Feel free to submit a pull request or open an issue to report bugs or suggest new features.
