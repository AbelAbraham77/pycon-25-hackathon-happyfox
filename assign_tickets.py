#!/usr/bin/env python3
"""
PyCon25 Hackathon: Intelligent Support Ticket Assignment System
================================================================

This system intelligently assigns support tickets to agents based on:
- Skill matching with ticket requirements
- Agent workload balancing
- Priority calculation based on urgency indicators
- Experience level weighting
- Availability status

Author: Abel Abraham
Date: September 2025
"""

import json
import re
import time
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Agent:
    """Agent data structure with methods for score calculation"""
    agent_id: str
    name: str
    skills: Dict[str, int]
    current_load: int
    availability_status: str
    experience_level: int
    
    def get_skill_score(self, skill_keyword: str) -> int:
        """Get skill level for a specific keyword, with fuzzy matching"""
        # Direct match first
        for skill, level in self.skills.items():
            if skill_keyword.lower() in skill.lower().replace('_', ' '):
                return level
        
        # Fuzzy matching for related skills
        skill_mappings = {
            'email': ['Microsoft_365'],
            'outlook': ['Microsoft_365'],
            'sharepoint': ['SharePoint_Online', 'Microsoft_365'],
            'teams': ['Microsoft_365'],
            'onedrive': ['Microsoft_365'],
            'microsoft 365': ['Microsoft_365'],
            'office 365': ['Microsoft_365'],
            'windows': ['Windows_OS', 'Windows_Server_2022'],
            'linux': ['Linux_Administration'],
            'database': ['Database_SQL'],
            'sql': ['Database_SQL'],
            'network': ['Networking', 'Network_Security'],
            'vpn': ['VPN_Troubleshooting', 'Networking'],
            'firewall': ['Firewall_Configuration', 'Network_Security'],
            'security': ['Network_Security', 'Endpoint_Security'],
            'malware': ['Antivirus_Malware', 'Endpoint_Security'],
            'phishing': ['Phishing_Analysis', 'Endpoint_Security'],
            'hardware': ['Hardware_Diagnostics'],
            'laptop': ['Laptop_Repair', 'Hardware_Diagnostics'],
            'printer': ['Printer_Troubleshooting'],
            'voip': ['Voice_VoIP'],
            'phone': ['Voice_VoIP'],
            'azure': ['Cloud_Azure'],
            'aws': ['Cloud_AWS'],
            'cloud': ['Cloud_Azure', 'Cloud_AWS'],
            'active directory': ['Active_Directory'],
            'ad': ['Active_Directory'],
            'dns': ['DNS_Configuration', 'Networking'],
            'ssl': ['SSL_Certificates'],
            'certificate': ['SSL_Certificates'],
            'powershell': ['PowerShell_Scripting'],
            'script': ['PowerShell_Scripting', 'Python_Scripting'],
            'python': ['Python_Scripting'],
            'mac': ['Mac_OS'],
            'macos': ['Mac_OS'],
            'api': ['API_Troubleshooting'],
            'web': ['Web_Server_Apache_Nginx'],
            'server': ['Web_Server_Apache_Nginx', 'Windows_Server_2022'],
            'samba': ['Linux_Administration'],
            'jenkins': ['DevOps_CI_CD'],
            'docker': ['Kubernetes_Docker'],
            'kubernetes': ['Kubernetes_Docker'],
            'switch': ['Switch_Configuration', 'Networking'],
            'router': ['Routing_Protocols', 'Networking'],
            'cisco': ['Cisco_IOS', 'Networking'],
            'monitoring': ['Network_Monitoring', 'SIEM_Logging'],
            'siem': ['SIEM_Logging'],
            'endpoint': ['Endpoint_Management', 'Endpoint_Security'],
            'virtualization': ['Virtualization_VMware'],
            'vmware': ['Virtualization_VMware'],
            'licensing': ['Software_Licensing'],
            'saas': ['SaaS_Integrations'],
            'integration': ['SaaS_Integrations'],
            'backup': ['Database_SQL', 'Linux_Administration'],
            'boot': ['Hardware_Diagnostics', 'Windows_OS'],
            'wifi': ['Networking', 'Network_Security'],
            'cable': ['Network_Cabling', 'Hardware_Diagnostics']
        }
        
        # Check direct keyword match first
        if skill_keyword.lower() in skill_mappings:
            for mapped_skill in skill_mappings[skill_keyword.lower()]:
                if mapped_skill in self.skills:
                    return self.skills[mapped_skill]
        
        # Check if keyword is contained in any mapping
        for keyword, mapped_skills in skill_mappings.items():
            if keyword in skill_keyword.lower() or skill_keyword.lower() in keyword:
                for mapped_skill in mapped_skills:
                    if mapped_skill in self.skills:
                        return self.skills[mapped_skill]
        
        return 0


@dataclass
class Ticket:
    """Ticket data structure with priority calculation"""
    ticket_id: str
    title: str
    description: str
    creation_timestamp: int
    
    def calculate_priority(self) -> int:
        """Calculate ticket priority based on urgency indicators"""
        priority = 1  # Base priority
        
        # Critical urgency indicators
        critical_keywords = [
            'critical', 'urgent', 'immediate', 'emergency', 'down', 'outage',
            'not working', 'failed', 'error', 'breach', 'security incident',
            'malware', 'attack', 'unauthorized', 'compromised', 'business-critical',
            'production', 'unable to work', 'completely', 'all users', 'major'
        ]
        
        # High priority indicators
        high_keywords = [
            'high', 'important', 'asap', 'soon', 'performance', 'slow',
            'degradation', 'affecting', 'multiple users', 'department',
            'deadline', 'presentation', 'meeting'
        ]
        
        # Medium priority indicators
        medium_keywords = [
            'medium', 'moderate', 'some users', 'intermittent', 'occasionally',
            'sometimes', 'specific user', 'one user'
        ]
        
        text = (self.title + ' ' + self.description).lower()
        
        # Count keyword occurrences
        critical_count = sum(1 for keyword in critical_keywords if keyword in text)
        high_count = sum(1 for keyword in high_keywords if keyword in text)
        medium_count = sum(1 for keyword in medium_keywords if keyword in text)
        
        # Calculate priority score
        if critical_count >= 2:
            priority = 5  # Critical
        elif critical_count >= 1:
            priority = 4  # High-Critical
        elif high_count >= 2:
            priority = 3  # High
        elif high_count >= 1 or medium_count >= 3:
            priority = 2  # Medium-High
        elif medium_count >= 1:
            priority = 2  # Medium
        
        # Age factor - older tickets get slight priority boost
        current_time = time.time()
        age_hours = (current_time - self.creation_timestamp) / 3600
        if age_hours > 24:
            priority += 1
        elif age_hours > 8:
            priority += 0.5
        
        return min(priority, 5)  # Cap at 5
    
    def extract_skill_keywords(self) -> List[str]:
        """Extract relevant skill keywords from ticket content"""
        text = (self.title + ' ' + self.description).lower()
        
        # Technology and skill keywords with more comprehensive matching
        keywords = [
            'vpn', 'email', 'outlook', 'sharepoint', 'teams', 'onedrive',
            'microsoft 365', 'office 365', 'windows', 'linux', 'database', 'sql',
            'network', 'firewall', 'security', 'malware', 'phishing', 'hardware',
            'laptop', 'printer', 'voip', 'phone', 'azure', 'aws', 'cloud',
            'active directory', 'dns', 'ssl', 'certificate', 'powershell',
            'script', 'python', 'mac', 'macos', 'api', 'web', 'server',
            'samba', 'jenkins', 'docker', 'kubernetes', 'switch', 'router',
            'cisco', 'monitoring', 'siem', 'endpoint', 'virtualization',
            'vmware', 'licensing', 'saas', 'integration', 'backup', 'boot',
            'wifi', 'cable', 'fan', 'memory', 'ram', 'disk space'
        ]
        
        found_keywords = []
        for keyword in keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        # Extract specific technology mentions with regex
        tech_patterns = [
            (r'microsoft\s+365', 'microsoft 365'),
            (r'office\s+365', 'microsoft 365'),
            (r'windows\s+\d+', 'windows'),
            (r'sql\s+server', 'sql'),
            (r'active\s+directory', 'active directory'),
            (r'exchange\s+server', 'email'),
            (r'sharepoint\s+online', 'sharepoint'),
            (r'office\s+suite', 'microsoft 365'),
            (r'xps\s+\d+', 'laptop'),
            (r'dell\s+latitude', 'laptop'),
            (r'macbook', 'mac'),
            (r'big\s+sur', 'mac'),
            (r'network\s+switch', 'switch'),
            (r'ip\s+address', 'network'),
            (r'dhcp\s+server', 'network'),
            (r'502\s+bad\s+gateway', 'web'),
            (r'503\s+service\s+unavailable', 'web'),
            (r'404\s+error', 'web'),
            (r'500\s+internal\s+server\s+error', 'web'),
            (r'single\s+sign.on', 'active directory'),
            (r'sso', 'active directory'),
            (r'saml', 'active directory')
        ]
        
        for pattern, keyword in tech_patterns:
            if re.search(pattern, text):
                if keyword not in found_keywords:
                    found_keywords.append(keyword)
        
        return found_keywords


class TicketAssignmentSystem:
    """Main system for intelligent ticket assignment"""
    
    def __init__(self, data_file: str):
        """Initialize the system with data from JSON file"""
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        self.agents = [Agent(**agent_data) for agent_data in data['agents']]
        self.tickets = [Ticket(**ticket_data) for ticket_data in data['tickets']]
        self.assignments = []
    
    def calculate_agent_score(self, agent: Agent, ticket: Ticket) -> Tuple[float, str]:
        """Calculate compatibility score between agent and ticket"""
        
        # 1. Skill matching score (60% weight - increased from 40%)
        skill_keywords = ticket.extract_skill_keywords()
        skill_scores = []
        matched_skills = []
        
        for keyword in skill_keywords:
            score = agent.get_skill_score(keyword)
            if score > 0:
                skill_scores.append(score)
                matched_skills.append(f"{keyword}({score})")
        
        if skill_scores:
            avg_skill_score = sum(skill_scores) / len(skill_scores)
            skill_match_bonus = len(skill_scores) * 1.0  # Increased bonus for multiple matches
        else:
            avg_skill_score = 0
            skill_match_bonus = 0
        
        skill_score = (avg_skill_score + skill_match_bonus) * 0.6  # Increased weight
        
        # 2. Workload balancing (20% weight - decreased from 25%)
        max_load = max(a.current_load for a in self.agents)
        min_load = min(a.current_load for a in self.agents)
        load_range = max_load - min_load if max_load > min_load else 1
        
        # Invert load score - lower load = higher score
        workload_score = ((max_load - agent.current_load) / load_range) * 20
        
        # 3. Experience level (15% weight - decreased from 20%)
        max_exp = max(a.experience_level for a in self.agents)
        experience_score = (agent.experience_level / max_exp) * 15
        
        # 4. Availability status (5% weight - decreased from 10%)
        availability_score = 5 if agent.availability_status == "Available" else 0
        
        # 5. Ticket priority boost (not counted in percentage, just additive)
        priority = ticket.calculate_priority()
        priority_bonus = priority * 0.5
        
        # Total score calculation
        total_score = skill_score + workload_score + experience_score + availability_score + priority_bonus
        
        # Generate rationale
        rationale = self._generate_rationale(
            agent, ticket, skill_score, matched_skills, 
            workload_score, experience_score, priority
        )
        
        return total_score, rationale
    
    def _generate_rationale(self, agent: Agent, ticket: Ticket, skill_score: float, 
                          matched_skills: List[str], workload_score: float, 
                          experience_score: float, priority: int) -> str:
        """Generate human-readable rationale for assignment"""
        
        rationale_parts = []
        
        # Primary reason
        if skill_score > 6:  # Strong skill match (adjusted threshold)
            # Extract skill names and scores for detailed rationale
            skill_details = []
            for skill_match in matched_skills:
                if '(' in skill_match:
                    skill_name = skill_match.split('(')[0]
                    skill_level = skill_match.split('(')[1].replace(')', '')
                    # Map skill names to actual agent skill names
                    for agent_skill, level in agent.skills.items():
                        if str(level) == skill_level and (skill_name.lower() in agent_skill.lower() or 
                            agent_skill.lower().replace('_', ' ') in skill_name.lower()):
                            skill_details.append(f"'{agent_skill}' ({level})")
                            break
            
            if skill_details:
                skill_text = f"strong skills in {' and '.join(skill_details[:2])}"
            else:
                skill_text = f"relevant expertise in {', '.join(matched_skills[:2])}"
            rationale_parts.append(f"Assigned to {agent.name} ({agent.agent_id}) based on {skill_text}")
        elif skill_score > 3:  # Moderate skill match (adjusted threshold)
            skill_details = []
            for skill_match in matched_skills:
                if '(' in skill_match:
                    skill_name = skill_match.split('(')[0]
                    skill_level = skill_match.split('(')[1].replace(')', '')
                    for agent_skill, level in agent.skills.items():
                        if str(level) == skill_level:
                            skill_details.append(f"'{agent_skill}' ({level})")
                            break
            
            if skill_details:
                skill_text = f"relevant skills in {' and '.join(skill_details[:2])}"
            else:
                skill_text = f"applicable skills in {', '.join(matched_skills[:2])}"
            rationale_parts.append(f"Assigned to {agent.name} ({agent.agent_id}) based on {skill_text}")
        else:
            rationale_parts.append(f"Assigned to {agent.name} ({agent.agent_id}) for general support")
        
        # Secondary factors
        secondary_factors = []
        
        if workload_score > 15:
            secondary_factors.append("low current workload")
        elif workload_score > 10:
            secondary_factors.append("moderate workload")
        
        if experience_score > 15:
            secondary_factors.append(f"high experience level ({agent.experience_level})")
        elif experience_score > 10:
            secondary_factors.append(f"good experience ({agent.experience_level})")
        
        if priority >= 4:
            secondary_factors.append("high priority ticket")
        elif priority >= 3:
            secondary_factors.append("medium-high priority")
        
        if secondary_factors:
            rationale_parts.append(f"considering {', '.join(secondary_factors)}")
        
        return ". ".join(rationale_parts) + "."
    
    def assign_tickets(self) -> List[Dict[str, Any]]:
        """Main method to assign all tickets to best matching agents"""
        
        # Sort tickets by priority (highest first)
        sorted_tickets = sorted(self.tickets, 
                              key=lambda t: t.calculate_priority(), 
                              reverse=True)
        
        # Track dynamic workload during assignment
        agent_loads = {agent.agent_id: agent.current_load for agent in self.agents}
        
        assignments = []
        
        for ticket in sorted_tickets:
            best_agent = None
            best_score = -1
            best_rationale = ""
            
            # Calculate scores for all available agents
            for agent in self.agents:
                if agent.availability_status != "Available":
                    continue
                
                # Update agent's current load for scoring
                temp_agent = Agent(
                    agent.agent_id, agent.name, agent.skills,
                    agent_loads[agent.agent_id], agent.availability_status,
                    agent.experience_level
                )
                
                score, rationale = self.calculate_agent_score(temp_agent, ticket)
                
                if score > best_score:
                    best_score = score
                    best_agent = agent
                    best_rationale = rationale
            
            # Assign ticket to best agent
            if best_agent:
                assignment = {
                    "ticket_id": ticket.ticket_id,
                    "title": ticket.title,
                    "assigned_agent_id": best_agent.agent_id,
                    "rationale": best_rationale
                }
                assignments.append(assignment)
                
                # Update agent's workload for next iteration
                agent_loads[best_agent.agent_id] += 1
            else:
                # Fallback assignment if no agents available
                fallback_agent = min(self.agents, key=lambda a: agent_loads[a.agent_id])
                assignment = {
                    "ticket_id": ticket.ticket_id,
                    "title": ticket.title,
                    "assigned_agent_id": fallback_agent.agent_id,
                    "rationale": f"Assigned to {fallback_agent.name} ({fallback_agent.agent_id}) as fallback with lowest current workload."
                }
                assignments.append(assignment)
                agent_loads[fallback_agent.agent_id] += 1
        
        return assignments
    
    def generate_output(self, output_file: str = "output_result.json"):
        """Generate and save the assignment results"""
        assignments = self.assign_tickets()
        
        output_data = {
            "assignments": assignments,
            "summary": {
                "total_tickets": len(self.tickets),
                "total_agents": len(self.agents),
                "assignments_made": len(assignments),
                "algorithm_version": "1.0",
                "features": [
                    "Intelligent skill matching with fuzzy logic",
                    "Dynamic workload balancing",
                    "Priority-based ticket ordering",
                    "Experience level weighting",
                    "Detailed assignment rationale"
                ]
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Assignment completed! Results saved to {output_file}")
        print(f"Processed {len(self.tickets)} tickets across {len(self.agents)} agents")
        
        # Print some statistics
        agent_assignment_count = defaultdict(int)
        for assignment in assignments:
            agent_assignment_count[assignment['assigned_agent_id']] += 1
        
        print("\nAssignment Distribution:")
        for agent in self.agents:
            count = agent_assignment_count[agent.agent_id]
            print(f"{agent.name} ({agent.agent_id}): {count} tickets")
        
        return assignments


def main():
    """Main execution function"""
    print("PyCon25 Hackathon: Intelligent Support Ticket Assignment System")
    print("=" * 65)
    
    # Initialize the system
    system = TicketAssignmentSystem("dataset.json")
    
    # Generate assignments
    assignments = system.generate_output()
    
    print(f"\nSuccessfully assigned {len(assignments)} tickets!")
    print("Check output_result.json for detailed results.")
if __name__ == "__main__":
    main()