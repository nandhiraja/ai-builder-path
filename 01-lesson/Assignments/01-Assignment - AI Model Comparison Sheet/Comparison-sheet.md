# Assignment 1 – AI Model Comparison Sheet

## Models Compared

* **GPT-4o** (OpenAI)
* **Claude Sonnet 4** (Anthropic)
* **Gemini Flash 2.0** (Google)
* **DeepSeek-R1:7B** (Local Model using Ollama)

---

# AI Model Comparison

| Criteria                      | GPT-4o    | Claude Sonnet 4 | Gemini Flash 2.0 | DeepSeek-R1:7B (Ollama) |
| ----------------------------- | --------- | --------------- | ---------------- | ----------------------- |
| **Code Quality**              | Excellent | Excellent       | Good             | Good                    |
| **SQL Generation**            | Excellent | Excellent       | Good             | Basic                   |
| **Infrastructure Automation** | Excellent | Excellent       | Good             | Basic                   |
| **Ease of Use**               | Excellent | Excellent       | Excellent        | Basic                   |
| **Speed / Latency**           | Good      | Good            | Excellent        | Good                    |

---

# 1. AppDev – Code Generation

| Model                | Rating    | Comments                                                                                                                                                                                |
| -------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GPT-4o**           | Excellent | Produces clean, well-structured, production-ready code. Strong support for ASP.NET Core, Entity Framework, Dapper, async programming, dependency injection, and common design patterns. |
| **Claude Sonnet 4**  | Excellent | Excellent for large codebases and maintaining consistency across multiple files. Follows instructions accurately, performs strong refactoring, and generates clear documentation.       |
| **Gemini Flash 2.0** | Good      | Generates code quickly and is useful for boilerplate, CRUD operations, and simple application logic. Complex business logic may require minor corrections.                              |
| **DeepSeek-R1:7B**   | Good      | Performs well for basic to intermediate coding tasks and provides useful explanations. May generate incorrect APIs or library references in more complex projects.                      |

---

# 2. Data – SQL Generation

| Model                | Rating    | Comments                                                                                                                                     |
| -------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **GPT-4o**           | Excellent | Generates accurate SQL including JOINs, CTEs, subqueries, window functions, stored procedures, and PostgreSQL-specific features.             |
| **Claude Sonnet 4**  | Excellent | Strong at schema-aware SQL generation, stored procedures, triggers, and explaining SQL logic in detail.                                      |
| **Gemini Flash 2.0** | Good      | Reliable for common SQL operations such as SELECT, INSERT, UPDATE, DELETE, and standard JOINs. Less reliable for advanced SQL logic.         |
| **DeepSeek-R1:7B**   | Basic     | Handles simple SQL queries correctly but struggles with advanced SQL features such as CTEs, stored procedures, and complex window functions. |

---

# 3. DevOps – Infrastructure Automation

| Model                | Rating    | Comments                                                                                                                                                           |
| -------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **GPT-4o**           | Excellent | Generates reliable Dockerfiles, Docker Compose files, Kubernetes manifests, GitHub Actions workflows, Terraform configurations, and automation scripts.            |
| **Claude Sonnet 4**  | Excellent | Produces well-structured infrastructure code with clear explanations. Strong for CI/CD pipelines, Docker, Kubernetes, Terraform, and Bash scripting.               |
| **Gemini Flash 2.0** | Good      | Very fast at generating YAML files, Kubernetes manifests, Docker configurations, and standard deployment templates. Better suited for common deployment scenarios. |
| **DeepSeek-R1:7B**   | Basic     | Can generate simple Dockerfiles and shell scripts but is limited for large cloud infrastructure and multi-service deployments.                                     |

---

# 4. Ease of Use

| Model                | Rating    | Comments                                                                                                                           |
| -------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **GPT-4o**           | Excellent | Easy to use with good documentation, API support, Playground access, and a large developer community.                              |
| **Claude Sonnet 4**  | Excellent | Excellent instruction following with a simple API and strong support for structured prompting.                                     |
| **Gemini Flash 2.0** | Excellent | Easy to test using Google AI Studio and integrates well with Google Cloud services.                                                |
| **DeepSeek-R1:7B**   | Basic     | Requires Ollama installation and local model download. Easy to use after setup but less beginner-friendly than cloud-based models. |

---

# 5. Speed / Latency

| Model                | Rating    | Comments                                                                                                                          |
| -------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **GPT-4o**           | Good      | Fast and consistent response time across most coding and development tasks.                                                       |
| **Claude Sonnet 4**  | Good      | Similar performance to GPT-4o but may be slightly slower for long responses due to more detailed reasoning.                       |
| **Gemini Flash 2.0** | Excellent | Fastest among the compared cloud models. Well suited for real-time applications and high-volume workloads.                        |
| **DeepSeek-R1:7B**   | Good      | Performance depends on local hardware. Since it runs locally, there is no network latency and data remains on the user's machine. |

---

# Overall Comparison

| Model                | Overall Rating (5) | Best For                                                                  | Main Limitation                                    |
| -------------------- | -------------- | ------------------------------------------------------------------------- | -------------------------------------------------- |
| **GPT-4o**           | 5          | Balanced coding, SQL, DevOps automation, and general software development | Paid API usage                                     |
| **Claude Sonnet 4**  | 5         | Large codebases, code reviews, documentation, and long-context tasks      | Slightly slower for very large responses           |
| **Gemini Flash 2.0** | 4           | Fast responses, rapid prototyping, and high-volume applications           | Less reliable for complex reasoning tasks          |
| **DeepSeek-R1:7B**   | 3            | Offline development, privacy-sensitive work, and learning                 | Limited capability compared to larger cloud models |

---

# Conclusion

Based on this comparison:

* **GPT-4o** provides the most balanced performance across code generation, SQL generation, and infrastructure automation, making it suitable for general software development.
* **Claude Sonnet 4** performs exceptionally well for large projects, code reviews, documentation, and tasks requiring long-context understanding.
* **Gemini Flash 2.0** is the best choice when speed and low latency are the primary requirements.
* **DeepSeek-R1:7B** is a good local alternative for offline development and privacy-focused environments, although it has limitations for advanced software engineering tasks.

---
