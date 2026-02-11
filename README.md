# Problem Domain
I am accustomed to creating RESTful APIs, particularly with Python libraries such requests or FastAPI. 
I desire to learn more about MCP servers and to become proficient in leveraging FastMCP as a tool to expose
APIs to AI/LLMs.

# Solution: Learning Project
Leverage the US National Weather Service Open Data APIs as a data source to build a simple MCP server.  

## Objectives
1. Utilize FastMCP to expose Weather Service Alerts API
2. Build out FastMCP with its additional parameters
   1. Resources
   2. Prompts

# The Plan
1. Build baseline functionality with Python requests
    - This will provide confirmation that weather alert data is successfully being returned from the Weather Service.
2. Add in my logging routines - transition print statements to proper logging methodology
3. Convert from Python request library to FastMCP
    - Perform validation testing
    - Connect with local AI clients - Claude and ChatGPT
4. Extend with additional FastMCP parameters: resources, prompts

# Learning Outcomes
- FastMCP makes the effort of exposing existing APIs to AI clients a relatively simple and straightforward exercise. One can disclose existing API functionality to non-technical and AI agents in a flexible and rapid deployment pattern.   
    - For example, the NWS weather alert API takes a State code as a parameter - effective, but limits how one interacts with the API. One needs to submit a correct state code via a designed UI to enable non-technical users to utilize the feature. 
    - With AI clients configured via a MCP server, one can merely as the question - “Are there any weather alerts in Minnesota?” - and the system will appropriately respond. 
    - In this scenario, the LLM will take the API’s response list of alerts (can be over 200) and summarize them into a discernible easy to understand text (less than 250 characters). 
    - This dramatically changes the UX, opening access who might be able to interact with existing APIs and improving their understanding of an API’s current response functionality without having to alter the base RESTful API. 
- The key lies in MCP server configuration and in crafting effective Tool descriptions, Resources, and Prompt scripts to assist and guideline the User Experience.
  - This creates further opportunities for enterprises’ external users - customers, suppliers, and stakeholders - to access in new channels and in potentially less technically-dependent manners.
  - Scenario 1: Dice's MCP server [https://www.dice.com/about/mcp]  makes it easier to query Dice's job search, but now presents challenges with how to interact with the resulting data. Organizations will need to consider existing the behavior of their API responses, how external users interact with them, and how a LLM might interact with structured data. In the case of the weather alert, the LLM's default behavior to summarize is appropriate. One needs to consider the UX and business rationale to understand how one might prompt and instruct the LLM on proper handling of API response data.  
  - Scenario 2: Consider the impact on data interoperability: How medical Payers might leverage data from an EHR will be different. Payers have their own internal business systems that utilize externally accessed data in specific business scenarios. Accessing a MCP servers will present the data in different ways, depending on the users prompt and the MCP server's prompts. An enterprise will need to specifically consider how accessing external APIs might impact and enhance existing internal business process and data pipelines. 
### Recommendations
1. Opportunities exist to extend existing API architecture to non-technical in business enterprises. MCP servers have the potential of reducing access barriers to data insights due to segregation of employee roles/duties/skills. Rather than requesting an engineering team to build new UIs and features around APIs, non-technical enterprise users can utilize AI clients to directly access existing data services - perhaps in new ways. 
1. When implementing MCP servers, technical personnel need to:
   1. Ensure proper configuration
      1. Great debugging tools exist: one needs to remember to install node.js and separately confirmed MCP Inspector
      1. Practically, some initial challenges were encountered configuring Claude Desktop to perform tests
         1. Was able to debug with Claude Desktop Developer logs and MCP Inspector (confirmed operations) 
         1. Resolved by editing claude_desktop_config.json to ensure all references were absolute references
1.  Spend effort on crafting tool descriptions, creating supporting resources, and designing effective prompts to ensure successful User Experiences. These represent the key value drivers and the determinants of performance and effectiveness.
1. Log, monitor, and evaluate the MCP server requests and the responses provided to the user to ensure the AI is providing accurate information aligned with the underlying API data services as well as the tool, resource, and prompt scripts. 
   1. The AI’s responses should not exaggerate the underlying API data but rather provide a human-oriented interpretation of the data in the API response. 
   1. Evaluation should be reviewed, monitored, and inspected to ensure AI clients do not engage in hyperbole but remain constrained by the API data services’ responses. 


### Additional items to learn:
1. Update to FastMCP 3.0  
2. Add resources and prompts capabilities
3. Simplify the MCP server file