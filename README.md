# PyCon25 Hackathon: Intelligent Support Ticket Assignment System

Welcome to the PyCon25 Hackathon project! 🚀

Once you are done with the hackathon, share your github link here: https://forms.gle/gnR62EoZUfeA8zqJ9

## 📋 Project Overview

### Problem Statement

In a helpdesk system, when customers raise support issues about different topics, we should ideally route tickets to agents who have knowledge and experience in solving that particular set of problems. However:

- **Volume Imbalance**: Not all topics have equal request volumes
- **Skill Gaps**: Not all agents have expertise in all areas
- **Fair Distribution**: Workload needs to be distributed equitably
- **Effective Resolution**: Tickets should go to the most capable agents

### Challenge

Build an optimal routing system that assigns support tickets to the best possible agent while ensuring:
- ✅ Maximum likelihood of successful resolution
- ✅ Fair distribution of workload across agents
- ✅ Effective prioritization of issues
- ✅ Cost-effective and scalable approach

## 📊 Data Structure

### Input: `dataset.json`
Contains two main sections:
- **Agents**: Support staff with skills, availability, and experience levels
- **Tickets**: Support requests with descriptions and timestamps

### Output: `output_result.json`
Your solution should generate ticket assignments with the following fields:

- **Mandatory:**
   - Ticket ID
   - Assigned Agent ID
- **Optional:**
   - Rationale/Justification for the assignment


## 🎯 Evaluation Criteria

Your solution will be judged on:

1. **Assignment Effectiveness** 
   - How well tickets are matched to agent skills
   - Likelihood of successful resolution

2. **Prioritization Strategy**
   - Creative use of ticket and agent attributes
   - Intelligent priority scoring

3. **Load Balancing**
   - Fair distribution of workload
   - Agent availability management

4. **Performance & Scalability**
   - Cost efficiency of the approach
   - Ability to handle large datasets

## 🏗️ Project Structure

```
pycon25-hackathon/
├── dataset.json           # Input data (agents and tickets)
├── output_result.json     # Expected output
├── README.md             # This file
└── [your solution files] # Your implementation
```

## 📈 Success Metrics

Your solution should optimize for:
- **Resolution Rate**: Tickets assigned to skilled agents
- **Response Time**: Efficient agent utilization
- **Workload Distribution**: Balanced assignment across team
- **Scalability**: Performance with increasing data size

## 🤝 Contributing

This is a hackathon project - unleash your creativity and build an innovative solution!

---

**Happy Hacking!** 🎉





