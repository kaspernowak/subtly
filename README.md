# Subtly - Open Source Subtitle Translation Platform

Subtly is an open-source subtitle translation platform that leverages DeepL's powerful translation API to provide high-quality subtitle translations. Built with modern web technologies, it allows users to translate subtitle files while managing their own DeepL API keys or using our subscription-based credit system.

## 🌟 Key Features

- 🎯 **Focused Subtitle Translation**
  - Support for SRT subtitle files (more formats coming soon)
  - High-quality translations powered by DeepL
  - No video file processing - purely subtitle-focused

- 💳 **Flexible Usage Options**
  - Use your own DeepL API key
  - Subscribe to our plans for monthly translation credits
  - Track character usage and remaining credits

- 🤝 **Open Source Community**
  - Contribute to improve translation logic
  - Add support for new subtitle formats
  - Help enhance the platform for everyone

## Technology Stack

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) Backend
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for database ORM
    - 🔍 [Pydantic](https://docs.pydantic.dev) for data validation
    - 💾 [PostgreSQL](https://www.postgresql.org) database
    - 🌐 [DeepL](https://www.deepl.com) API integration for translations

- 🚀 [Nuxt 3](https://nuxt.com) for the frontend
    - 💃 Using TypeScript, Vue 3 Composition API, and Nitro server
    - 🎨 [Nuxt UI](https://ui.nuxt.com) for the frontend components
    - 🤖 Auto-imported components and composables
    - 🧪 [Playwright](https://playwright.dev) for End-to-End testing
    - 🦇 Dark mode support

- 🛸 [**Traefik**](https://traefik.io) for reverse proxy and load balancing

- 🔒 Security & User Management
    - Secure authentication system
    - API key management
    - Usage tracking and quotas
    - Subscription handling

- 🐋 Deployment
    - Docker Compose setup for easy deployment
    - Production-ready configuration
    - Scalable architecture

## Getting Started

### Prerequisites

- Docker and Docker Compose
- DeepL API key (for development)
- Python 3.8+
- Node.js 16+

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kaspernowak/subtly.git
   cd subtly
   ```

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your settings:
   - `DEEPL_API_KEY`: Your DeepL API key
   - `SECRET_KEY`: Generate a secure key for JWT tokens
   - `FIRST_SUPERUSER` and `FIRST_SUPERUSER_PASSWORD`: Admin credentials
   - `POSTGRES_PASSWORD`: Database password
   - For development, the default values for hosts and ports should work

4. Start the development environment:
   ```bash
   docker-compose up -d
   ```

### Environment Configuration

The project uses environment variables for configuration. Key variables include:

- `ENVIRONMENT`: Set to `local`, `staging`, or `production`
- `DOMAIN`: Used by Traefik for traffic routing and TLS certificates
- `FRONTEND_HOST`: Used for generating links in emails
- `BACKEND_CORS_ORIGINS`: Allowed origins for CORS
- `DEEPL_API_KEY`: Your DeepL API key for translations

For a complete list of configuration options, see `.env.example`.

## Contributing

We welcome contributions! Whether you're fixing bugs, improving translation logic, adding new subtitle format support, or enhancing documentation, your help is valuable.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution

- Adding support for new subtitle formats
- Improving translation accuracy and handling
- Enhancing the user interface
- Adding new features
- Improving documentation
- Writing tests

## License

The Subtly - Open Source Subtitle Translation Platform is licensed under the terms of the MIT license.

## Support and Community

- [GitHub Issues](https://github.com/kaspernowak/subtly/issues) for bug reports and feature requests
- [GitHub Discussions](https://github.com/kaspernowak/subtly/discussions) for questions and community discussions

## Acknowledgments

- [DeepL](https://www.deepl.com) for providing the translation API
- All our contributors and community members
