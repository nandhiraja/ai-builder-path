### Smart Gmail Agent with n8n

Build an n8n agent that classifies incoming queries and routes emails to the right users.

**Setup:**

- Integrate an **HTTP Request** tool making a `GET` request to:
`https://api.escuelajs.co/api/v1/users`
This returns mock users with different roles (customer / admin)

**Agent Behavior — based on query classification:**

| Query Type | Category | Example |
| --- | --- | --- |
| Product Inquiry, General Support, Sales Question, Billing Inquiry, Feature Request | **Customer** | *"I was charged twice for this month's subscription. Can someone from billing review my account and process a refund for the duplicate charge?"* |
| Technical Escalation, System Issue, Security Concern, Data Issue, Integration Problem | **Admin** | *"URGENT: Our API integration is down and affecting production systems. We need immediate technical support to resolve this critical issue."* |

The agent should send the email only to users matching the classified role.


## Output preview
### Flow
<img width="864" height="460" alt="Image" src="https://github.com/user-attachments/assets/bc26c72e-a867-44f7-b4ab-10ac1dc8f084" />

--- 
### Customers 
<img width="384" height="593" alt="Image" src="https://github.com/user-attachments/assets/9c6ed844-cbeb-446b-8b79-5b7349399037" />

---
### Admin
<img width="377" height="254" alt="Image" src="https://github.com/user-attachments/assets/594e713f-df53-45b8-b084-a6763e4482bd" />