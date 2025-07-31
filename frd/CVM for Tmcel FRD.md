

# **Functional Requirements Document: A Customer Value Management Platform for Tmcel**

## **Executive Summary**

This document outlines the functional and non-functional requirements for the development of a new Customer Value Management (CVM) platform for Moçambique Telecom, SA (Tmcel). The strategic rationale for this project is rooted in the urgent need to address Tmcel's critical financial position and enhance its competitive standing within the dynamic Mozambican telecommunications market. The platform is envisioned as a mission-critical investment designed to reverse significant financial losses, which reached nearly €60 million in 2024, and to counteract a state of negative equity amounting to €195.9 million.1

The core problem confronting Tmcel is an inability to effectively monetize its customer base and the substantial capital investments made in network modernization. Despite upgrading 1,248 cell sites and increasing backbone capacity to 400 Gbps, the company has struggled to translate these technical capabilities into revenue growth and profitability.1 It currently lacks the sophisticated data analytics, personalization, and automated campaign tools that its primary competitors, Vodacom and Movitel, leverage to maintain market dominance.3 This capability gap has left Tmcel vulnerable, competing on increasingly unsustainable price points in a market of approximately 18.91 million mobile connections.6

The proposed solution is a state-of-the-art CVM platform, built upon Tmcel's existing Customer Data Platform (CDP) and developed using a modern, high-performance technology stack: a Next.js, TypeScript, and Tailwind CSS frontend; a Python backend using the FastAPI framework; and a PostgreSQL database. This platform will serve as the central intelligence hub for all customer interactions, providing a 360-degree customer view, advanced machine learning-driven segmentation, personalized campaign orchestration across multiple channels, and robust analytics for performance measurement and strategy refinement.

The implementation of this CVM platform will directly target measurable improvements in key performance indicators (KPIs). The primary business outcomes include a significant reduction in customer churn, a sustainable increase in Average Revenue Per User (ARPU) through intelligent upselling and cross-selling, and a marked improvement in the return on investment (ROI) for marketing campaigns. By enabling a strategic shift from mass-market promotions to data-driven, personalized value propositions, the CVM platform will empower Tmcel to compete more effectively, stabilize its financial performance, and build a foundation for long-term, profitable growth. This document provides the detailed specifications necessary for the successful development and deployment of this transformative system.

## **Part 1: Strategic Context and Business Objectives**

### **1.1 The Case for Transformation: Tmcel's Strategic Imperative**

The initiative to develop and deploy a comprehensive Customer Value Management (CVM) platform is not a discretionary marketing project for Tmcel; it is a fundamental strategic imperative driven by acute financial distress and the need to secure the company's long-term viability. The context for this transformation is defined by three critical factors: a deepening financial crisis, a lagging position in customer acquisition and market share, and the urgent need to monetize recent, large-scale infrastructure investments.

**Financial Crisis:** Tmcel's financial performance represents an existential threat to the organization. In 2024, the state-owned operator reported staggering losses of 4.441 billion meticais (approximately €59.7 million), a figure that had doubled from the already substantial losses of €28.6 million recorded in 2023\.1 This deteriorating performance has culminated in negative equity of 14.563 billion meticais (€195.9 million), a clear indicator of severe financial instability. An independent audit by EY highlighted that these conditions raise significant doubts about the company's ability to continue as a going concern.1 This financial backdrop makes it clear that incremental improvements are insufficient. A transformational tool that can directly impact revenue generation and customer retention is required to alter this trajectory.

**Stagnant Customer Growth and Market Position:** While Tmcel managed to grow its active mobile client base from 717,052 in 2023 to 841,171 in 2024, this figure represents a very small fraction of the total Mozambican market.1 As of early 2024, Mozambique had an estimated 18.91 million active cellular connections.6 This disparity underscores Tmcel's minor market share compared to its dominant rivals, Vodacom and Movitel.8 The company is failing to effectively attract new subscribers and, more critically, lacks the mechanisms to maximize the value of its existing customer base. In a hyper-competitive, multi-SIM environment where customers frequently switch between operators for the best deals 4, the absence of a robust CVM strategy to build loyalty and increase stickiness is a fatal flaw.

**Monetizing Infrastructure Investments:** After a period described as "almost 10 years without investment," Tmcel has embarked on a significant network modernization and expansion program, part of a $132 million revitalization plan.1 This has involved modernizing or activating 1,248 cell sites and increasing its broadband backbone capacity from 10 Gbps to 400 Gbps.1 While these upgrades are essential for providing competitive 4G services and improving quality, they are fundamentally capital expenditures that, on their own, do not generate revenue. The escalating financial losses demonstrate that improved network capability does not automatically translate to improved financial performance. The CVM platform is the missing link—the software "brain" required to monetize this new hardware. It will enable Tmcel to identify customers in newly upgraded 4G coverage areas and target them with relevant high-speed data offers, manage network load through dynamic pricing, and create compelling product bundles that leverage the enhanced network capacity. Without this monetization engine, the massive capital outlay on infrastructure risks yielding a deeply insufficient return on investment, further exacerbating the company's financial crisis.

### **1.2 The Mozambican Telecommunications Battlefield**

To design an effective CVM platform for Tmcel, it is crucial to understand the unique characteristics of the Mozambican market, including its size, demographics, digital behaviors, and the powerful influence of its regulatory body.

**Market Size, Penetration, and Demographics:** The Mozambican market comprises a population of approximately 34.37 million people, with 18.91 million active mobile connections as of early 2024\.6 This results in a mobile penetration rate of 55.0%, which, while growing, suggests that there is still significant potential for market expansion. However, a key challenge is the low internet penetration rate, which stands at only 23.2%, meaning 7.96 million users are online while over 26 million remain offline.6 This digital divide presents both a challenge and a major opportunity for data service growth, a key area the CVM platform must target. The market's demographic profile is profoundly young, with a median age of just 17.1 years and 64% of the population under the age of 25\.7 This demographic reality must inform every aspect of the CVM strategy, from the design of product bundles (e.g., social media-focused data packs) to the mechanics of loyalty programs (e.g., gamification) and the choice of communication channels.

**Digital Behavior:** Consumer digital life in Mozambique is dominated by a few key platforms. Facebook is the leading social network with 3.2 million users, followed by the rapidly growing TikTok with 1.46 million users.6 A GeoPoll survey confirms that 93% of smartphone users use Facebook and 81% use WhatsApp.10 These platforms are not just communication tools; they are primary channels for marketing, customer engagement, and potentially service delivery. The CVM platform must therefore be designed with capabilities to integrate with these social media APIs for targeted advertising and customer interaction.

**The Regulatory Environment and its Strategic Implications:** The Mozambican telecommunications sector is overseen by a highly active and interventionist regulator, the Instituto Nacional das Comunicações de Moçambique (INCM). The INCM's recent actions have fundamentally reshaped the competitive landscape. In May 2024, the regulator took the decisive step of banning all "unlimited" voice and data packages offered by operators, citing the need to avoid a "collapse of the market" and prevent "unfair competition".11 This intervention was likely a response to an aggressive price war that would have disproportionately harmed the financially weakest player, Tmcel.

This regulatory move, while seemingly restrictive, creates a significant strategic opportunity. By establishing price floors and eliminating the simplest form of value proposition ("unlimited everything"), the INCM has shifted the basis of competition from pure price to perceived value. Operators can no longer win simply by being the cheapest; they must now win by being the smartest. They must construct nuanced, segmented offers that provide the best combination of data, voice, and value-added services for specific customer needs and price sensitivities. This is precisely the environment where a sophisticated CVM platform excels. It allows an operator to move beyond one-size-fits-all tariffs and compete on intelligence, using data to craft highly personalized and relevant bundles (e.g., "1GB of data plus unlimited WhatsApp and Facebook access for 24 hours" for a young user, or "a voice-heavy package with a small data allowance" for a rural user). The CVM platform is thus Tmcel's primary weapon to capitalize on this new regulatory paradigm and challenge its larger rivals on a more level playing field. Furthermore, the INCM's mandate for a Unique Telecommunications Number (NUTEL) for every subscriber provides a stable, unique identifier that will be foundational for the CVM platform's data model, ensuring accurate customer tracking across services and devices.12

### **1.3 Competitive CVM Intelligence**

Tmcel operates in a market defined by two powerful competitors, Vodacom and Movitel, each with a distinct and effective strategy for customer value management. The proposed CVM platform must not only match but strategically counter their capabilities.

#### **1.3.1 Vodacom's "TechCo" Playbook**

Vodacom, the market leader with nearly 50% share 8, is pursuing a sophisticated strategy of transitioning from a traditional telecommunications company ("TelCo") into a diversified technology company ("TechCo").3 This strategy is built on a "system of advantage," where core connectivity is bundled with a rich digital ecosystem of financial services, e-commerce, and lifestyle offerings to create deep customer lock-in.14

The engine of this strategy is a dedicated focus on "Personalisation through CVM and Big Data".3 Vodacom has made substantial investments in a world-class Big Data platform that analyzes over 3,000 attributes per customer to generate a 360-degree view.4 This allows them to move beyond price-based competition and create personalized "next-best offers" tailored to individual behaviors and needs.

Their flagship CVM product is the **"Just4U"** platform, which delivers personalized deals on airtime, data, and messages. This platform has achieved significant traction, with 28% of their Mozambican customer base actively participating.4 Furthermore, their CVM capabilities are deeply integrated into their behavioral loyalty program,

**"VodaBucks,"** which rewards engagement and has been shown to increase the number of active days customers spend on the network.4 Central to their ecosystem is the

**M-Pesa** mobile money platform, which Vodacom plans to expand aggressively into a full-fledged financial services suite offering savings, loans, insurance, and wealth management, creating a powerful barrier to churn.15

#### **1.3.2 Movitel's Grassroots Dominance**

Movitel, a joint venture involving Vietnam's Viettel Group, has achieved remarkable success by pursuing a fundamentally different strategy focused on grassroots expansion and affordability.16 Their model is to "popularize telecom services," with a specific focus on rural and underserved areas that were historically neglected by competitors.5 This was achieved through massive initial investment in network infrastructure, giving them the widest network coverage in the country, with 2,800 towers and 25,000 km of fiber optic cable.5

Movitel's CVM approach is less about hyper-personalization and more about accessibility and community integration. They employ "low and flexibly tailored tariff plans" to match the budgets of low-income users and utilize a unique "door-to-door" sales and support model with nearly 4,000 direct sales staff to reach customers in remote villages.5 Their brand loyalty is further strengthened through extensive social programs, most notably providing free internet to over 2,500 schools, positioning themselves as a partner in national development.5 Their mobile money service,

**e-Mola**, is a cornerstone of their strategy and has seen explosive growth, reaching nearly 6 million users by early 2024, demonstrating their success in bundling financial services with core connectivity.9

#### **Table 1: Competitive CVM Feature Matrix**

The following table provides a comparative analysis of CVM capabilities, highlighting the gaps the new Tmcel platform must address to achieve competitive parity and differentiation.

| Feature / Capability | Tmcel (Current State) | Vodacom (Target State) | Movitel (Target State) | Proposed Tmcel CVM Platform |
| :---- | :---- | :---- | :---- | :---- |
| **Data & Analytics** |  |  |  |  |
| 360° Customer View | Limited, siloed data | Yes (3,000+ attributes) 4 | Basic profile data | Yes, via CDP integration |
| Real-Time Data Processing | No | Yes (for NBO) 3 | Limited (for MFS) 16 | Yes (FastAPI, WebSockets) |
| Predictive Analytics (Churn/LTV) | No | Yes (Big Data platform) 13 | No (Focus on affordability) | Yes (ML models) |
| **Segmentation** |  |  |  |  |
| Rule-Based Segmentation | Manual, basic | Yes | Yes (Geographic, basic) | Yes (Visual, advanced) |
| RFM Segmentation | No | Yes | No | Yes (Automated) |
| ML-Driven Micro-segmentation | No | Yes 13 | No | Yes (Predictive segments) |
| **Personalization** |  |  |  |  |
| Personalized Bundles | No | Yes (Just4U platform) 4 | Limited (Tailored tariffs) 5 | Yes (NBO Engine) |
| Next Best Offer (NBO) Engine | No | Yes 4 | No | Yes (ML-driven) |
| **Campaigns** |  |  |  |  |
| Multi-Channel Orchestration | No (Siloed channels) | Yes (Omnichannel focus) 14 | Limited (SMS, direct sales) | Yes (SMS, Push, USSD, etc.) |
| A/B/n Testing & Control Groups | No | Yes | No | Yes (Integrated framework) |
| **Loyalty** |  |  |  |  |
| Points-Based Program | Limited (e.g., Bónus Aniversário) 19 | Yes (VodaBucks) 4 | No (Focus on social programs) | Yes (Points & Rewards Catalog) |
| Gamification | No | Limited | No | Yes (Badges, Streaks) |
| **Financial Services** |  |  |  |  |
| Integrated Mobile Money | No (No proprietary service) | Yes (M-Pesa) 15 | Yes (e-Mola) 9 | Future integration required |
| Airtime Lending | Yes (Empresta-la) 20 | Yes | Yes | Yes (Integrate & enhance) |
| **Regulatory** |  |  |  |  |
| Dynamic Tariff/Rules Engine | No | Ad-hoc | Ad-hoc | Yes (INCM compliance) |

### **1.4 Business Goals and Success Metrics**

The CVM platform's success will be measured against specific, quantifiable business objectives that directly address the strategic challenges outlined above. The platform's analytics module must be designed to track these goals through a defined set of Key Performance Indicators (KPIs).

**Primary Goals (Year 1 Post-Launch):**

* **Reduce Postpaid Churn:** Decrease the monthly postpaid churn rate by a minimum of 15% from the baseline established pre-launch. This will be achieved through proactive retention campaigns triggered by predictive churn scores.  
* **Increase Prepaid ARPU:** Increase the average monthly revenue per prepaid user (ARPU) by 10%. This will be driven by personalized upselling of data bundles and value-added services (VAS) identified by the Next Best Offer engine.  
* **Improve Campaign Conversion:** Achieve a 20% uplift in conversion rates for campaigns executed through the CVM platform compared to the baseline performance of traditional mass-market campaigns. This will be measured using A/B testing with control groups.

**Secondary Goals (Year 2 Post-Launch):**

* **Increase Data Penetration:** Increase the percentage of the active subscriber base that regularly uses mobile data services by 25%, converting voice-only users into data consumers.  
* **Drive Loyalty Program Adoption:** Achieve an active participation rate of 30% in the new loyalty program among the addressable subscriber base.  
* **Operational Efficiency:** Reduce the end-to-end time required for campaign planning, building, and execution by 40%, freeing up marketing resources for more strategic tasks.

**Key Performance Indicators (KPIs):** The platform's analytics dashboards (specified in FR-AN) must provide clear, real-time visualization of the following KPIs:

* **Retention Metrics:** Churn Rate (prepaid and postpaid), Customer Lifetime Value (CLV), Active Days on Network.  
* **Monetization Metrics:** Average Revenue Per User (ARPU), Data Usage per User (in MB), Revenue per Campaign.  
* **Engagement Metrics:** Offer Redemption Rate, Campaign Conversion Rate (by channel and segment), Loyalty Program Enrollment and Engagement Rate.

## **Part 2: System Overview and High-Level Architecture**

### **2.1 Platform Vision**

The Tmcel CVM Platform will be the central nervous system for all customer-facing value propositions. It is envisioned to be more than a marketing automation tool; it will be an intelligence engine that transforms vast streams of raw customer data from the existing Customer Data Platform (CDP) and other real-time sources into actionable, revenue-generating strategies. The platform will enable Tmcel to fundamentally shift its operational model from reactive, product-centric mass marketing to a proactive, customer-centric approach focused on building long-term relationships and maximizing lifetime value. It will empower the business to understand each customer as an individual, predict their needs, and engage them with the right offer, through the right channel, at the right moment.

### **2.2 Architectural Principles**

The design and development of the CVM platform will be guided by a set of core architectural principles to ensure it is robust, scalable, secure, and future-proof.

* **Privacy-by-Design:** Every feature, data model, and API will be architected with the complex patchwork of Mozambican data protection principles as a foundational requirement, not a subsequent addition. This includes adhering to provisions from the Constitution, the Electronic Transactions Law, and other relevant statutes to ensure full compliance from inception.21  
* **Real-Time & Asynchronous:** The architecture will be fundamentally asynchronous, leveraging the capabilities of Python's FastAPI framework.24 This is critical for low-latency ingestion of real-time event streams (e.g., recharges, location changes) and for enabling "in-the-moment" marketing triggers, such as delivering an offer the instant a user enters a new 4G coverage area.  
* **Scalability & Elasticity:** The system must be designed to horizontally scale to handle the entire Tmcel subscriber base (currently 841,171 and projected to grow) and process millions of daily events without performance degradation. The architecture will be built on containerization (Docker) and orchestrated by Kubernetes, allowing for the elastic scaling of individual microservices based on load.26  
* **Modularity & Extensibility:** To avoid creating a monolithic, inflexible system, the platform will be architected as a collection of loosely coupled microservices. Core functions such as the Segmentation Engine, Campaign Orchestrator, and Analytics Service will be developed as independent components with well-defined APIs. This approach facilitates parallel development, independent deployment, and makes the system easier to maintain and extend with new functionalities in the future.  
* **Data-Driven Closed Loop:** The platform will operate on a continuous feedback loop. All actions and decisions, from segment creation to offer selection, will be based on data and analytics. The results of every campaign will be fed back into the system to refine predictive models and inform future strategies, creating a cycle of continuous improvement.

### **2.3 System Context Diagram**

The following diagram illustrates the CVM platform's position within the broader Tmcel technology ecosystem, showing its key data sources, execution channels, and user groups.

\+---------------------------+       \+---------------------------+       \+-------------------------+

| Inbound Data Sources | | | | Outbound Channels |  
|---------------------------| | | |-------------------------|  
| \<--API--\> | | | | \<--API--\> |  
| \<--Stream-\>| | | | \<--API--\>|  
| \[Network Probes\] \<--Stream-\>|------\>| Tmcel CVM Platform |------\>| \<--API--\>|  
| \<--API--\> | | (FastAPI Backend) | | \<--API--\> \[Cust. Care\] |  
| \[Mobile App\]    \<--Stream-\>| | | | \<--API--\> |  
\+---------------------------+ | | \+-------------------------+

| |  
                                    \+-------------^-------------+  
|  
| UI via HTTPS  
|  
                                    \+-------------v-------------+

| Frontend (Next.js) |  
|---------------------------|  
| |  
| \[CVM Analysts\] |  
| |  
                                    \+---------------------------+

* **Inbound Data Sources:** The platform will consume data from various systems. The **Customer Data Platform (CDP)** will be the primary source for unified, static customer profiles. **Billing & Charging Systems**, **Network Probes** (for UDRs and location data), and the **Tmcel Mobile App** will provide real-time event streams. The **CRM System** will provide historical customer interaction data.  
* **Outbound Execution Channels:** The platform will trigger actions through multiple channels, including **SMS** and **USSD Gateways**, a **Push Notification Service** for the mobile app, the **Customer Care Portal** (to display Next Best Offers to agents), and **Social Media APIs** (e.g., Facebook/Meta Ads API) for targeted digital campaigns.  
* **Internal Users:** Various internal teams, including **Marketing**, **CVM Analysts**, and **System Administrators**, will interact with the platform through a secure, web-based frontend.

### **2.4 Core Technology Stack**

The selection of the core technology stack is based on the user's preference and is well-aligned with the platform's architectural principles, particularly the need for performance, scalability, and a rich data science ecosystem.

* **Frontend:** **Next.js with React, TypeScript, and Tailwind CSS.**  
  * **Rationale:** This combination provides a best-in-class framework for building modern, interactive, and highly performant web applications. Next.js offers server-side rendering (SSR) and static site generation (SSG) for fast initial page loads, which is crucial for complex dashboards. TypeScript ensures type safety, reducing bugs and improving maintainability in a large codebase. Tailwind CSS enables rapid development of a consistent and responsive user interface.  
* **Backend:** **Python 3.9+ with FastAPI.**  
  * **Rationale:** FastAPI is chosen for its exceptional performance, which rivals that of NodeJS and Go, and its native support for asynchronous operations (async/await).25 This is non-negotiable for a system that must process real-time data streams. Furthermore, Python's mature and extensive ecosystem of libraries for data science and machine learning (e.g., Pandas, Scikit-learn, MLflow) is essential for building the platform's predictive analytics and NBO capabilities.30  
* **Database:** **PostgreSQL (version 14+).**  
  * **Rationale:** PostgreSQL is a powerful, open-source, and highly reliable object-relational database. It is well-suited for this project due to its robustness, ACID compliance, and advanced features. Its support for JSONB data types is ideal for storing flexible, semi-structured customer profiles and event data. Additionally, extensions like PostGIS can be leveraged for sophisticated location-based segmentation in the future.  
* **API Architecture:** The platform will expose a dual API architecture.  
  * **RESTful APIs:** For all standard create, read, update, and delete (CRUD) operations, such as managing campaigns, segments, and users. This provides a well-understood, stateless interface for the frontend.  
  * **WebSockets:** For real-time, bidirectional communication. This will be used to push live updates to the analytics dashboards (e.g., campaign progress) and to send real-time notifications to logged-in users, providing a highly interactive experience without the need for constant polling.24

## **Part 3: User Roles and Permissions**

A robust Role-Based Access Control (RBAC) system is fundamental to ensuring the security and operational integrity of the CVM platform. The system must enforce the principle of least privilege, granting users access only to the data and functionalities necessary to perform their designated roles.

### **3.1 Persona Definitions**

The platform will support several distinct user personas, each with a specific set of responsibilities and corresponding access rights.

* **CVM Analyst:** This user is responsible for data exploration, hypothesis testing, and performance analysis. They need to understand customer behavior, identify valuable segments, and measure the impact of marketing activities. Their primary focus is on insight generation. They will have read-only access to most data and analytics modules but will not be permitted to create or launch campaigns.  
* **Marketing Campaign Manager:** This user is the primary operator of the platform's campaign functionalities. They are responsible for the end-to-end lifecycle of a marketing campaign: designing the customer journey, building the target segment, defining the offers, creating the communication templates, scheduling the launch, and monitoring the execution. They require full create, read, update, and delete (CRUD) permissions within the segmentation and campaign management modules.  
* **Business Intelligence (BI) Lead:** This user is responsible for creating and maintaining high-level reports and dashboards for executive and management stakeholders. They need to be able to aggregate performance data and present it in a clear, concise format. They will have full access to the analytics module, including the ability to build custom reports, but will have limited access to individual customer data.  
* **System Administrator:** This user is responsible for the technical health and configuration of the platform. Their duties include managing user accounts and permissions, configuring integrations with external systems (like SMS gateways), and overseeing system settings. They will have full administrative access to the platform's configuration but will have restricted or masked access to personally identifiable information (PII) to maintain data privacy.  
* **Compliance Officer:** This is a specialized, read-only role designed to ensure the platform operates within the bounds of Mozambican law. This user must have access to all audit logs, consent management records, and data subject rights request workflows to perform regular audits and verify compliance with regulations like the Electronic Transactions Law and the Constitution.21 They cannot modify data or launch campaigns.

### **3.2 Role-Based Access Control (RBAC) Matrix**

The following matrix provides a detailed specification for the permissions assigned to each user role across the platform's key modules and features. The development team must implement this matrix to enforce the RBAC policies.

| Module / Feature | CVM Analyst | Marketing Campaign Manager | BI Lead | System Administrator | Compliance Officer |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Dashboard & Analytics** |  |  |  |  |  |
| View Main Dashboard | R | R | R | R | R |
| View Campaign Reports | R | R | R | R | R |
| Create Custom Reports | R | R | C/R/U/D | R | R |
| Export Report Data | R | R | R | R | R |
| **Data Management** |  |  |  |  |  |
| View Customer Profiles (Masked PII) | R | R | No Access | R | R |
| View Full Customer PII | No Access | No Access | No Access | No Access | R (audited) |
| **Segmentation** |  |  |  |  |  |
| View Segments | R | R/U/D | R | R | R |
| Create/Edit Segments | No Access | C/R/U/D | No Access | No Access | No Access |
| **Campaign & Offer Management** |  |  |  |  |  |
| View Campaigns & Offers | R | C/R/U/D | R | R | R |
| Create/Edit Campaigns | No Access | C/R/U/D | No Access | No Access | No Access |
| Approve Campaign for Launch | No Access | R (Request) | No Access | No Access | No Access |
| Launch Campaign | No Access | C (Execute) | No Access | No Access | No Access |
| **Compliance & Administration** |  |  |  |  |  |
| Manage User Accounts & Roles | No Access | No Access | No Access | C/R/U/D | No Access |
| Configure System Integrations | No Access | No Access | No Access | C/R/U/D | No Access |
| View Audit Logs | No Access | No Access | No Access | R | R |
| Manage Consent Records | No Access | No Access | No Access | No Access | R |
| Service Data Subject Rights | No Access | No Access | No Access | No Access | R/U (Execute) |

*Legend: C=Create, R=Read, U=Update, D=Delete*

## **Part 4: Detailed Functional Requirements**

This section details the specific functional requirements for each module of the CVM platform. Each requirement is assigned a unique identifier for traceability throughout the development and testing lifecycle.

### **4.1 FR-DM: Data Management & Enrichment**

This module is the foundation of the CVM platform, responsible for ingesting, processing, and maintaining the rich customer data needed for all other functions.

* **FR-DM-001: Unified Customer Profile Synchronization.** The system shall integrate with the existing central Customer Data Platform (CDP) to create and maintain a unified profile for each subscriber. This will involve two synchronization mechanisms: a nightly batch process to ingest full profile snapshots and a real-time, event-driven API to receive immediate updates for critical data changes.  
* **FR-DM-002: Real-Time Event Ingestion Pipeline.** The system shall expose a high-throughput, low-latency event ingestion endpoint, architected around a message queue (see Part 6 for recommendations like RabbitMQ or Kafka). This endpoint must be capable of receiving and processing a continuous stream of customer events from various sources, including but not limited to:  
  * Call Detail Records (CDRs) from the network switches.  
  * Data Usage Records (UDRs) detailing internet sessions.  
  * Real-time recharge events from the billing and top-up systems.  
  * Location updates from cell tower handoffs.  
  * In-app events from the Tmcel mobile application (e.g., screen views, button clicks).  
* **FR-DM-003: Calculated CVM Metrics.** The system shall automatically calculate, store, and maintain a set of key CVM metrics for each customer profile. These metrics must be updated in near real-time as new events are ingested. The initial set of mandatory metrics includes:  
  * **Recency, Frequency, Monetary (RFM) scores:** Classic marketing metrics to gauge customer engagement and value.  
  * **Average Revenue Per User (ARPU):** Calculated over rolling 30, 60, and 90-day windows.  
  * **Days Since Last Activity (DSLA):** A key indicator of potential churn.  
  * **Primary Handset Type:** Derived from network data (e.g., TAC codes). This is critical for device-specific offers, given the diverse device market in Mozambique where brands like Samsung, Xiaomi, and Tecno have significant share.34  
  * **Predictive Customer Lifetime Value (pCLV):** A forward-looking metric generated by an ML model.  
  * **Predictive Churn Score:** The output of a churn prediction model, indicating the probability of a customer leaving the network.  
* **FR-DM-004: Offer Interaction History.** The system must maintain a comprehensive historical log for each customer, detailing every offer that has been presented to them, whether they accepted or rejected it, the channel of communication, and the timestamp of the interaction. This history is crucial for the Next Best Offer engine and for preventing offer fatigue.

### **4.2 FR-SEG: Customer Segmentation Engine**

This module provides the tools for marketers and analysts to group customers into meaningful segments for targeted communication.

* **FR-SEG-001: Visual Segmentation Builder.** The user interface for creating segments must be intuitive and visual. It shall provide a drag-and-drop canvas where users can combine various attributes and conditions using logical operators (AND, OR, NOT) to build complex segmentation rules without writing any code.  
* **FR-SEG-002: Multi-Attribute Rule-Based Segmentation.** The segmentation engine must support the creation of static segments based on any attribute available in the unified customer profile. This includes demographic data (age, gender, location), calculated CVM metrics (from FR-DM-003), historical behavior (e.g., products purchased), and device information. For example, a user must be able to create a segment such as: "Postpaid customers aged 18-24, using a 4G-capable Samsung device 34, with an ARPU greater than 500 MZN, who have not purchased an additional data bundle in the last 30 days."  
* **FR-SEG-003: Dynamic, Trigger-Based Segments.** The system shall support the creation of dynamic segments where customers are automatically added or removed based on real-time event triggers. This enables "in-the-moment" marketing. Examples include:  
  * A "Welcome" segment that a new customer enters immediately upon network activation.  
  * A "High-Speed Interest" segment for users who enter a 4G/LTE coverage zone for the first time.  
  * A "Low Balance" segment for prepaid users whose balance drops below a predefined threshold.  
* **FR-SEG-004: Predictive, ML-Driven Segments.** The system must be able to define segments based on the output of machine learning models. This requires seamless integration with the ML model serving infrastructure (see Part 6). This allows for the creation of highly valuable, forward-looking segments that are impossible to define with rules alone, such as:  
  * "High-Value, High-Risk": Subscribers with a high pCLV but also a churn probability greater than 80%.  
  * "Potential Upgraders": Subscribers identified by an ML model as most likely to respond to a 4G device upgrade offer or a postpaid plan migration.  
* **FR-SEG-005: Real-Time Segment Sizing.** As a user builds or modifies a segment's rules in the UI, the system must query the database in the background and display an updated, real-time count of the number of customers who match the criteria. This provides immediate feedback and allows for rapid iteration on segment definitions.

### **4.3 FR-CM: Campaign & Offer Management**

This module is the action-oriented core of the platform, enabling marketers to design, test, execute, and manage personalized marketing campaigns.

* **FR-CM-001: Multi-Step, Omni-Channel Campaign Journeys.** The system shall provide a visual journey builder that allows marketers to design complex, multi-step campaigns that span multiple communication channels. For example, a journey could be defined as: *"Day 1: Send SMS with Offer A. If user clicks link but does not purchase, wait 24 hours. Day 2: Send a follow-up push notification with a slight discount. If user opens the app, display a personalized in-app message. If user does not respond after 3 days, exit journey."*  
* **FR-CM-002: Next Best Offer (NBO) Engine.** The platform must include a sophisticated NBO engine. This is a critical capability to counter Vodacom's "Just4U" platform.4 For any given customer and context (e.g., at the moment of recharge, or when their data bundle is about to expire), the NBO engine will use ML models to analyze their profile and predict the single best offer to present. The engine's recommendation will be a function of maximizing the probability of acceptance while also aligning with business objectives (e.g., maximizing revenue, driving data usage).  
* **FR-CM-003: A/B/n Testing and Control Groups.** The platform must have a built-in, statistically rigorous A/B/n testing framework. Campaign managers must be able to easily configure tests to compare the performance of multiple variables, such as different offers, communication copy, subject lines, or channels. Crucially, the system must support the automatic creation of a "control group" for every campaign—a statistically significant portion of the target segment that receives no communication. This is the only way to accurately measure the true incremental lift and ROI of a campaign.  
* **FR-CM-004: Centralized Offer Library.** The system shall include a centralized library for defining and managing all marketable products, services, bundles, and discounts. Each offer will have configurable attributes such as name, description, price, validity period, and the technical provisioning command required to activate it on the billing system.  
* **FR-CM-005: Business and Regulatory Rules Engine.** This is a critical component for operational control and compliance. The campaign module must be governed by a powerful and highly configurable rules engine that enforces constraints before any campaign is launched. This engine must manage:  
  * **Budgetary Controls:** Set spending limits for campaigns or individual offers.  
  * **Contact Policy:** Enforce frequency caps (e.g., "No more than one marketing SMS per customer in a 48-hour period").  
  * **Channel Preference:** Respect customer-stated preferences for communication channels (e.g., "SMS only, no push notifications").  
  * **INCM Tariff Compliance:** This is a non-negotiable requirement. The rules engine must be able to model the minimum price floors for voice, data, and SMS as mandated by the INCM.11 It must automatically prevent any campaign manager from creating or launching an offer that violates these regulatory tariffs.

### **4.4 FR-LOY: Loyalty and Gamification**

This module is designed to increase customer engagement, stickiness, and emotional connection to the Tmcel brand, directly responding to the sophisticated loyalty programs of competitors and the preferences of Mozambique's young demographic.7

* **FR-LOY-001: Points-Based Loyalty Framework.** The system shall provide the backend framework for a comprehensive points-based loyalty program. It must be able to define rules for earning points, such as points awarded per metical of recharge, for purchasing specific data bundles, for consecutive days of network activity, or for engaging with the mobile app.  
* **FR-LOY-002: Redeemable Rewards Catalog.** The platform will host a "Rewards Catalog" where loyalty points can be redeemed. This catalog must be configurable by the marketing team and support a variety of reward types, including:  
  * **Telco Products:** Free data bundles, voice minutes, SMS packages.  
  * **Discounts:** Vouchers for discounts on handset purchases or future recharges.  
  * **Partner Offers:** (Future capability) Discounts on third-party services like streaming, food delivery, etc.  
* **FR-LOY-003: Gamification Mechanics.** To drive engagement, particularly among younger users, the system must support common gamification mechanics. This includes:  
  * **Badges & Achievements:** Awarding digital badges for completing specific actions (e.g., a "Data Guru" badge for using over 5GB in a month, a "Loyal Friend" badge for referring a new customer).  
  * **Streaks & Challenges:** Implementing time-based challenges that reward consistent behavior (e.g., "Recharge at least 50 MZN every week for four consecutive weeks to unlock a bonus 1GB data bundle").  
* **FR-LOY-004: 'Bónus Aniversário' Integration.** The system must automate and manage the existing 'Bónus Aniversário' (Birthday Bonus) program. It will track each customer's "anniversary" date (date of first activation) and automatically check for eligibility based on the defined business rule: the customer must have a total spend equal to or greater than 1000 MZN within the preceding 30-day period to receive the bonus.19

### **4.5 FR-AN: Analytics & Reporting**

This module provides the tools to measure performance, generate insights, and demonstrate the value of the CVM program to the business.

* **FR-AN-001: Real-Time CVM Dashboard.** The platform shall feature a central, high-level dashboard that provides an at-a-glance view of key CVM health metrics. This dashboard will be built using the Next.js frontend and will receive live data updates from the FastAPI backend via WebSockets to ensure the information is always current.24 It must display KPIs such as: total active users, daily/weekly/monthly churn rates, blended ARPU, and a summary of active campaigns and their conversion rates.  
* **FR-AN-002: Detailed Campaign Performance Reporting.** For every campaign executed through the platform, the system must automatically generate a comprehensive performance report. This report must be drillable and include metrics such as:  
  * **Funnel Metrics:** Sent, Delivered, Opened, Clicked, Converted.  
  * **Financial Metrics:** Cost per acquisition (CPA), Revenue Generated, Return on Investment (ROI).  
  * **Breakdowns:** Performance broken down by customer segment, communication channel, offer type, and A/B test variant.  
* **FR-AN-003: Customer Journey Visualization.** The system shall provide analytics tools that allow a CVM Analyst to visualize and understand common customer journeys. This could involve Sankey diagrams or flow charts that map the typical paths customers take, for example, from their first recharge, to their first data bundle purchase, to periods of inactivity, and eventual churn or retention.  
* **FR-AN-004: Cohort Analysis.** The platform must include a powerful cohort analysis tool. This will allow analysts to group customers based on a common characteristic (e.g., all customers who joined in January 2025\) and track their behavior and value over time. This is essential for understanding long-term trends, such as comparing the 90-day LTV of customers acquired through a social media campaign versus those acquired through a retail channel.

## **Part 5: Non-Functional Requirements**

Non-functional requirements (NFRs) define the quality attributes of the system. They are as critical as functional requirements for the success of the platform, ensuring it is performant, secure, compliant, and reliable.

### **5.1 NFR-PERF: Performance & Scalability**

* **NFR-PERF-001: API Response Time.** All synchronous, user-facing API endpoints must have a 95th percentile response time of less than 200 milliseconds under the expected peak load.  
* **NFR-PERF-002: Event Ingestion Throughput.** The real-time event ingestion pipeline (as defined in FR-DM-002) must be architected to handle a minimum sustained load of 10,000 events per second, with an end-to-end processing latency (from ingestion to availability for segmentation) of less than 2 seconds.  
* **NFR-PERF-003: Concurrent User Load.** The platform must comfortably support at least 50 concurrent internal users (CVM Analysts, Campaign Managers) interacting with the system (building segments, creating campaigns, viewing dashboards) without any perceptible degradation in UI responsiveness or backend performance.

### **5.2 NFR-SEC: Security**

* **NFR-SEC-001: Data-at-Rest Encryption.** All customer data stored within the PostgreSQL database, including backups, must be encrypted at rest using a strong, industry-standard algorithm such as AES-256.  
* **NFR-SEC-002: Data-in-Transit Encryption.** All data transmitted over the network must be encrypted. This includes communication between the user's browser and the frontend server, between the frontend and the backend APIs, and all inter-service communication between microservices. TLS 1.2 or a higher version must be enforced for all connections.  
* **NFR-SEC-003: User Authentication.** User authentication must not be handled by a custom-built solution. The platform shall integrate with a centralized, corporate identity provider using standard protocols like OAuth 2.0 or OpenID Connect to handle user login and session management, enabling Single Sign-On (SSO).  
* **NFR-SEC-004: Comprehensive Audit Logging.** The system must maintain a detailed, immutable audit log of all significant user actions. This log must capture the user ID, timestamp, action performed, and the affected resource. Actions to be logged must include, at a minimum: user logins/logouts, viewing of PII, creation/modification of segments and campaigns, and the launching of any campaign.

### **5.3 NFR-COMP: Regulatory Compliance & Data Privacy**

Navigating Mozambique's legal framework for data privacy is a critical challenge. Unlike jurisdictions with a single, comprehensive data protection law like the GDPR, Mozambique's regulations are a "legal patchwork" spread across multiple statutes.8 This means compliance cannot be an afterthought; it must be deeply embedded in the system's architecture. The platform must be designed to explicitly address the specific requirements of the Constitution, the Electronic Transactions Law, and other relevant legislation to ensure it is fully compliant and auditable.

* **NFR-COMP-001: Granular Consent Management.** The system must implement a robust consent management module. For every customer, the platform must be able to store and manage their consent status for receiving marketing communications. This record must be granular, capturing the specific channel consented to (e.g., SMS, Push), the precise legal basis for contact, a timestamp of when consent was given, and an easy mechanism for withdrawal. This is essential to comply with the direct marketing provisions of the Electronic Transactions Law, which require prior consent.22  
* **NFR-COMP-002: Data Subject Rights Servicing.** The platform must provide a dedicated internal interface for the Compliance Officer to service Data Subject Rights requests, as guaranteed by Article 71 of the Constitution.23 This interface must support, at a minimum:  
  * **Right to Access:** A function to generate a complete, human-readable report of all personal data held by the CVM platform for a specific subscriber, identified by their phone number or NUTEL ID.  
  * **Right to Rectification:** A mechanism to find and correct any inaccurate personal data for a specific subscriber upon a verified request.  
* **NFR-COMP-003: Sensitive Data Processing Controls.** The system must enforce the strict prohibitions on processing certain categories of sensitive personal data as stipulated by the Mozambican Constitution. The platform must be architected to prevent the storage or use of individually identifiable information concerning a person's political, philosophical, or ideological beliefs, religious faith, or trade union affiliation for segmentation or marketing purposes.21  
* **NFR-COMP-004: Access Control and Auditing.** To comply with the prohibitions against unauthorized access to third-party data found in the Electronic Transactions Law 37, the system must enforce the RBAC matrix (Section 3.2) strictly. All access to personal data, particularly by administrative or compliance roles, must be logged in the audit trail (NFR-SEC-004) to deter misuse and provide a clear record for regulatory review.

#### **Table 2: Data Subject Rights Compliance Mapping**

This table provides a clear mapping from legal obligations to platform features, ensuring auditable compliance.

| Legal Right | Source (Legal Article) | Required Platform Feature(s) | Verification Method |
| :---- | :---- | :---- | :---- |
| Right to Privacy, Honour, Reputation | Constitution, Art. 41 23 | RBAC (Sec 3.2), Audit Logs (NFR-SEC-004) | Review user permissions and access logs for unauthorized PII access. |
| Right to Access Personal Data | Constitution, Art. 71 23 | "Data Access Report" feature for Compliance Officer | Generate a complete data report for a test subject and verify its contents. |
| Right to Rectify Data | Constitution, Art. 71 23 | "Data Correction" interface for Compliance Officer | Correct a data field (e.g., name spelling) for a test subject and verify the change in the database. |
| Consent for Direct Marketing | Electronic Transactions Law 22 | Consent Management Module (NFR-COMP-001) | Test opt-in and opt-out functionality; verify that consent status is respected by the campaign engine and that all actions are timestamped and logged. |
| Data Security Obligation | Electronic Transactions Law, Art. 63 37 | Encryption (NFR-SEC-001, NFR-SEC-002), Access Controls (RBAC) | Perform security audit and penetration testing to verify encryption and access control implementation. |

### **5.4 NFR-AVAIL: Availability & Reliability**

* **NFR-AVAIL-001: System Uptime.** The CVM platform, including all its user-facing and data-processing components, must be designed for high availability with a target uptime of 99.95%, excluding planned maintenance windows.  
* **NFR-AVAIL-002: Geographic Redundancy.** To ensure resilience against infrastructure failures, the entire platform shall be deployed across a minimum of two separate physical availability zones within the chosen cloud provider's infrastructure.  
* **NFR-AVAIL-003: Database Resiliency and Recovery.** The PostgreSQL database must be configured in a high-availability setup with a primary instance and at least one hot-standby replica in a separate availability zone, with automated failover. Full database backups must be performed daily, and point-in-time recovery (PITR) must be enabled. Backups must be retained for a minimum of 30 days.

## **Part 6: Recommended Ancillary Technologies**

The core technology stack (Next.js, FastAPI, PostgreSQL) provides a strong foundation. However, to build a truly enterprise-grade CVM and MLOps platform, a set of ancillary tools is required to handle specific functions like real-time messaging, workflow orchestration, and model management. The following table provides justified recommendations for these complementary technologies.

#### **Table 3: Recommended Ancillary Technologies**

| Category | Recommended Tool(s) | Rationale & Integration with Core Stack |
| :---- | :---- | :---- |
| **Real-Time Messaging / Event Streaming** | **RabbitMQ** or **Apache Kafka** | Essential for implementing the real-time event ingestion pipeline (FR-DM-002) and for decoupling microservices. RabbitMQ is simpler to set up for moderate loads, while Kafka offers higher throughput and durability for massive event streams. FastAPI can easily integrate with either via libraries like aio-pika or aiokafka. |
| **ML Experiment Tracking** | **MLflow** | The open-source industry standard for managing the end-to-end machine learning lifecycle. It is critical for tracking, comparing, and versioning the experiments used to develop the predictive churn and LTV models (FR-SEG-004). Its Python-native integration makes it a natural fit for the FastAPI backend and associated data science workflows.40 |
| **ML Model Serving** | **BentoML** or **Native FastAPI Endpoints** | Required to deploy the trained ML models (churn, NBO) as production-ready APIs. BentoML is a specialized framework that simplifies the process of packaging models and their dependencies into optimized Docker containers for serving.41 For simpler models, FastAPI's native performance allows for direct serving within the main application. |
| **Workflow Orchestration** | **Prefect** or **Apache Airflow** | Necessary for scheduling, executing, and monitoring complex, recurring data pipelines. This includes the nightly batch ingestion from the CDP (FR-DM-001) and the periodic retraining and validation of ML models. Both tools are Python-based and provide robust dependency management and error handling.31 |
| **Monitoring & Observability** | **Prometheus & Grafana Stack** | The de-facto open-source standard for systems and application monitoring. Prometheus will be used to scrape and store time-series metrics from all platform components (NFR-PERF), while Grafana will be used to build dashboards for visualizing system health, application performance, and setting up alerts. This is essential for maintaining high availability (NFR-AVAIL-001). |
| **Container Orchestration** | **Kubernetes (K8s)** | The definitive standard for deploying, scaling, and managing containerized applications in production. Using Kubernetes is non-negotiable for meeting the platform's scalability (NFR-PERF-003) and availability (NFR-AVAIL-002) requirements. It provides automated scaling, self-healing, and service discovery for the platform's microservices.26 |
| **CI/CD Pipeline** | **GitHub Actions** or **Jenkins** | Automation of the software delivery lifecycle is crucial for development velocity and reliability. A CI/CD pipeline will be configured to automatically build Docker images, run unit and integration tests, and deploy changes to staging and production environments on Kubernetes upon code commits. |

## **Part 7: High-Level Implementation Roadmap**

The development of the CVM platform will be executed in a phased approach, prioritizing the delivery of core functionalities first to demonstrate value quickly, followed by the rollout of more advanced capabilities.

### **Phase 1: Minimum Viable Product (MVP) \- The Foundation (Target: 3-4 Months)**

* **Focus:** Establish the core data pipeline, enable basic segmentation, and launch single-channel campaigns to prove the fundamental concept.  
* **Features to Implement:**  
  * Core data ingestion and synchronization from the CDP (FR-DM-001).  
  * The visual, rule-based segmentation engine (FR-SEG-001, FR-SEG-002, FR-SEG-005).  
  * Basic campaign creation and execution for the SMS channel only (subset of FR-CM-001).  
  * A foundational campaign performance dashboard showing send/delivery/conversion rates (subset of FR-AN-001).  
  * Essential compliance features: consent management for SMS and the data subject access request interface (NFR-COMP-001, NFR-COMP-002).  
* **Primary Goal:** To launch the first set of targeted SMS campaigns to well-defined customer segments and demonstrate a measurable uplift in conversion rates compared to previous mass-market SMS blasts.

### **Phase 2: Advanced Analytics & Personalization (Target: 4-6 Months)**

* **Focus:** Introduce machine learning and more sophisticated analytics to move from reactive to proactive value management.  
* **Features to Implement:**  
  * The real-time event ingestion pipeline (FR-DM-002).  
  * Development and integration of the first ML models for predictive churn and LTV scoring, enabling ML-driven segments (FR-SEG-004).  
  * The full A/B/n testing framework with control group support (FR-CM-003).  
  * The initial version of the Next Best Offer (NBO) engine (FR-CM-002).  
  * Advanced analytics dashboards, including customer journey visualization and cohort analysis (FR-AN-003, FR-AN-004).  
* **Primary Goal:** To begin proactively identifying and targeting at-risk customers with retention offers and to increase ARPU by personalizing upsell offers based on NBO recommendations.

### **Phase 3: Omni-Channel Orchestration & Loyalty (Target: 4-6 Months)**

* **Focus:** Expand the platform's reach across all key customer touchpoints and build long-term loyalty and emotional engagement.  
* **Features to Implement:**  
  * Integration with additional execution channels: Push Notifications, USSD, and In-App Messaging, enabling full omni-channel journey orchestration (FR-CM-001).  
  * The complete loyalty and gamification platform, including points, rewards, badges, and challenges (FR-LOY-001 to FR-LOY-004).  
  * API integration to display Next Best Offers to agents within the customer care portal.  
* **Primary Goal:** To create a seamless and consistent customer experience across all digital touchpoints and to build a powerful loyalty program that increases customer stickiness and provides a strong competitive differentiator against Vodacom and Movitel.

## **Conclusion**

The development of this Customer Value Management platform represents a pivotal moment for Tmcel. Faced with severe financial pressures and intense market competition, a strategic pivot from a traditional, network-focused operator to a modern, customer-centric technology company is not merely an option, but a necessity for survival and future growth. The detailed requirements laid out in this document provide a comprehensive blueprint for building the engine that will drive this transformation.

By leveraging a modern, high-performance technology stack and adhering to a phased, value-driven implementation plan, Tmcel can deploy a platform capable of directly addressing its most pressing business challenges. The system will enable the monetization of recent infrastructure investments, provide the intelligence to compete effectively in a market where value has superseded price, and build lasting relationships with Mozambique's young and digitally-native population. The successful execution of this project will empower Tmcel to reduce churn, increase customer lifetime value, and ultimately, build a sustainable and profitable future.

#### **Works cited**

1. Mobile Operator Tmcel Posts Nearly €60M in Losses in 2024 \- 360 Mozambique, accessed July 29, 2025, [https://360mozambique.com/innovation/telecom/mobile-operator-tmcel-posts-nearly-e60m-in-losses-in-2024/](https://360mozambique.com/innovation/telecom/mobile-operator-tmcel-posts-nearly-e60m-in-losses-in-2024/)  
2. WIOCC and Tmcel partner to boost Mozambique's digital backbone \- Developing Telecoms, accessed July 29, 2025, [https://developingtelecoms.com/telecom-technology/optical-fixed-networks/18824-wiocc-and-tmcel-partner-to-boost-mozambique-s-digital-backbone.html](https://developingtelecoms.com/telecom-technology/optical-fixed-networks/18824-wiocc-and-tmcel-partner-to-boost-mozambique-s-digital-backbone.html)  
3. Our strategy | What we do | Vodacom Group, accessed July 29, 2025, [https://www.vodacom.com/our-strategy.php](https://www.vodacom.com/our-strategy.php)  
4. Personalisation through CVM and Big Data \- Vodacom Group, accessed July 29, 2025, [https://vodacom.com/pdf/what-we-do/2022/personalisation-through-cvm-and-big-data.pdf](https://vodacom.com/pdf/what-we-do/2022/personalisation-through-cvm-and-big-data.pdf)  
5. Movitel – An evidence of Viettel's successful business model in Africa \- pan african visions, accessed July 29, 2025, [https://panafricanvisions.com/2014/08/movitel-evidence-viettels-successful-business-model-africa/](https://panafricanvisions.com/2014/08/movitel-evidence-viettels-successful-business-model-africa/)  
6. Digital 2024: Mozambique — DataReportal – Global Digital Insights, accessed July 29, 2025, [https://datareportal.com/reports/digital-2024-mozambique](https://datareportal.com/reports/digital-2024-mozambique)  
7. How Many Mozambicans Have Internet Access and Which Social Networks Are Most Popular? \- 360 Mozambique, accessed July 29, 2025, [https://360mozambique.com/trends/how-many-mozambicans-have-internet-access-and-which-social-networks-are-most-popular/](https://360mozambique.com/trends/how-many-mozambicans-have-internet-access-and-which-social-networks-are-most-popular/)  
8. Mozambique-Country-Report.pdf \- Paradigm Initiative, accessed July 29, 2025, [https://paradigmhq.org/wp-content/uploads/2024/06/Mozambique-Country-Report.pdf](https://paradigmhq.org/wp-content/uploads/2024/06/Mozambique-Country-Report.pdf)  
9. Viettel Global climbs to top spot in Mozambique \- Nhan Dan Online, accessed July 29, 2025, [https://en.nhandan.vn/viettel-global-climbs-to-top-spot-in-mozambique-post135904.html](https://en.nhandan.vn/viettel-global-climbs-to-top-spot-in-mozambique-post135904.html)  
10. Project Last Mile \- Smartphone and Social Media Usage Landscape in Mozambique, accessed July 29, 2025, [https://www.geopoll.com/blog/mozambique-smartphone-social-media-report/](https://www.geopoll.com/blog/mozambique-smartphone-social-media-report/)  
11. Mozambique : Telecom regulator INCM bans unlimited data and voice packages, to avoid “collapse of the market”, accessed July 29, 2025, [https://clubofmozambique.com/news/mozambique-telecom-regulator-incm-bans-unlimited-data-and-voice-packages-to-avoid-collapse-of-the-market-257971/](https://clubofmozambique.com/news/mozambique-telecom-regulator-incm-bans-unlimited-data-and-voice-packages-to-avoid-collapse-of-the-market-257971/)  
12. Mozambique \- Digital Economy \- International Trade Administration, accessed July 29, 2025, [https://www.trade.gov/country-commercial-guides/mozambique-digital-economy](https://www.trade.gov/country-commercial-guides/mozambique-digital-economy)  
13. Our approach to value creation \- vodacom-reports.co.za, accessed July 29, 2025, [https://vodacom-reports.co.za/integrated-reports/ir-2024/documents/Our-approach-to-value-creation.pdf](https://vodacom-reports.co.za/integrated-reports/ir-2024/documents/Our-approach-to-value-creation.pdf)  
14. Our strategy \- vodacom-reports.co.za, accessed July 29, 2025, [https://vodacom-reports.co.za/integrated-reports/ir-2022/documents/Our-strategy.pdf](https://vodacom-reports.co.za/integrated-reports/ir-2022/documents/Our-strategy.pdf)  
15. Vodacom Targets 32 Million New Mobile Money Users by 2030 \- Ecofin Agency, accessed July 29, 2025, [https://www.ecofinagency.com/news-digital/2105-46922-vodacom-targets-32-million-new-mobile-money-users-by-2030](https://www.ecofinagency.com/news-digital/2105-46922-vodacom-targets-32-million-new-mobile-money-users-by-2030)  
16. Market penetration of telecom- munication EMNCs in Africa: The case of Viettel Global in Mozambique \- Theseus, accessed July 29, 2025, [https://www.theseus.fi/bitstream/10024/815077/3/Le\_Thi%20Mai%20Lien.pdf](https://www.theseus.fi/bitstream/10024/815077/3/Le_Thi%20Mai%20Lien.pdf)  
17. Movitel becomes bright spot in Vietnam-Mozambique cooperation, accessed July 29, 2025, [https://en.vietnamplus.vn/movitel-becomes-bright-spot-in-vietnam-mozambique-cooperation-post255432.vnp](https://en.vietnamplus.vn/movitel-becomes-bright-spot-in-vietnam-mozambique-cooperation-post255432.vnp)  
18. President of Mozambique calls on Viettel to train technology experts for the country, accessed July 29, 2025, [https://viettel.com.vn/en/news-events/news/president-of-mozambique-calls-on-viettel-to-train-technology-experts-for-the-country/](https://viettel.com.vn/en/news-events/news/president-of-mozambique-calls-on-viettel-to-train-technology-experts-for-the-country/)  
19. Bónus Aniversário \- Tmcel, accessed July 29, 2025, [https://www.tmcel.mz/bonus-aniversario/](https://www.tmcel.mz/bonus-aniversario/)  
20. Tmcel Tmcel \- Moçambique Telecom, accessed July 29, 2025, [https://www.tmcel.mz/](https://www.tmcel.mz/)  
21. FACTSHEET: MOZAMBIQUE | Data Protection Africa, accessed July 29, 2025, [https://dataprotection.africa/wp-content/uploads/2019/10/Mozambique-Factsheet-1.pdf](https://dataprotection.africa/wp-content/uploads/2019/10/Mozambique-Factsheet-1.pdf)  
22. MOZAMBIQUE \- International Bar Association, accessed July 29, 2025, [https://www.ibanet.org/document?id=Digital-Regulations-in-the-Metaverse-Era-Mozambique](https://www.ibanet.org/document?id=Digital-Regulations-in-the-Metaverse-Era-Mozambique)  
23. CONSTITUTION OF THE REPUBLIC OF MOZAMBIQUE, accessed July 29, 2025, [https://www.legal-tools.org/doc/7d56b4/pdf/](https://www.legal-tools.org/doc/7d56b4/pdf/)  
24. Real-Time Applications with WebSockets and FastAPI | by Joël-Steve N. | Stackademic, accessed July 29, 2025, [https://blog.stackademic.com/real-time-applications-with-websockets-and-fastapi-7f9ea66bcddf](https://blog.stackademic.com/real-time-applications-with-websockets-and-fastapi-7f9ea66bcddf)  
25. Concurrency and async / await \- FastAPI, accessed July 29, 2025, [https://fastapi.tiangolo.com/async/](https://fastapi.tiangolo.com/async/)  
26. Deploying FastAPI and PostgreSQL Microservices to Kubernetes using Minikube, accessed July 29, 2025, [https://developers.eksworkshop.com/docs/python/kubernetes/deploy-app/](https://developers.eksworkshop.com/docs/python/kubernetes/deploy-app/)  
27. Deploying a FastAPI Application on Kubernetes: A Step-by-Step Guide for Production, accessed July 29, 2025, [https://sumanta9090.medium.com/deploying-a-fastapi-application-on-kubernetes-a-step-by-step-guide-for-production-d74faac4ca36](https://sumanta9090.medium.com/deploying-a-fastapi-application-on-kubernetes-a-step-by-step-guide-for-production-d74faac4ca36)  
28. Deployments Concepts \- FastAPI, accessed July 29, 2025, [https://fastapi.tiangolo.com/deployment/concepts/](https://fastapi.tiangolo.com/deployment/concepts/)  
29. Real-time Data Processing with FastAPI \- Harness the Power of FastAPI for Real-time Applications \- OnEggy Technologies, accessed July 29, 2025, [https://www.oneggy.com/service/real-time-data-processing-with-fastapi](https://www.oneggy.com/service/real-time-data-processing-with-fastapi)  
30. FastAPI Python Tutorial: Build an Analytics API from Scratch \- YouTube, accessed July 29, 2025, [https://www.youtube.com/watch?v=tiBeLLv5GJo](https://www.youtube.com/watch?v=tiBeLLv5GJo)  
31. MLOps and LLMOps with Python: A Comprehensive Guide with Tools and Best Practices | by André Castro | Medium, accessed July 29, 2025, [https://medium.com/@andreluizfc/mlops-and-llmops-with-python-a-comprehensive-guide-with-tools-and-best-practices-b696b5e7b58d](https://medium.com/@andreluizfc/mlops-and-llmops-with-python-a-comprehensive-guide-with-tools-and-best-practices-b696b5e7b58d)  
32. What are the options to build a realtime API in Python? \- Reddit, accessed July 29, 2025, [https://www.reddit.com/r/webdev/comments/1bfig67/what\_are\_the\_options\_to\_build\_a\_realtime\_api\_in/](https://www.reddit.com/r/webdev/comments/1bfig67/what_are_the_options_to_build_a_realtime_api_in/)  
33. Mozambique | Jurisdictions \- DataGuidance, accessed July 29, 2025, [https://www.dataguidance.com/jurisdictions/mozambique](https://www.dataguidance.com/jurisdictions/mozambique)  
34. Mobile Vendor Market Share Mozambique | Statcounter Global Stats, accessed July 29, 2025, [https://gs.statcounter.com/vendor-market-share/mobile/mozambique](https://gs.statcounter.com/vendor-market-share/mobile/mozambique)  
35. Mozambique 2004 (rev. 2007\) Constitution, accessed July 29, 2025, [https://www.constituteproject.org/constitution/Mozambique\_2007](https://www.constituteproject.org/constitution/Mozambique_2007)  
36. Data protection laws in Mozambique, accessed July 29, 2025, [https://www.dlapiperdataprotection.com/index.html?t=law\&c=MZ](https://www.dlapiperdataprotection.com/index.html?t=law&c=MZ)  
37. Mozambique(English).pdf, accessed July 29, 2025, [https://info.ushijima-law.gr.jp/hubfs/pi\_legislation/Mozambique(English).pdf](https://info.ushijima-law.gr.jp/hubfs/pi_legislation/Mozambique\(English\).pdf)  
38. Mozambique \- Data Breach Guide \- World Law Group, accessed July 29, 2025, [https://www.theworldlawgroup.com/membership/news/mozambique-data-breach-guide](https://www.theworldlawgroup.com/membership/news/mozambique-data-breach-guide)  
39. Electronic Transactions in the Mozambican Legal System \- CMS in Mozambique, accessed July 29, 2025, [https://www.cga.co.mz/en/moz/publication/electronic-transactions-in-the-mozambican-legal-system](https://www.cga.co.mz/en/moz/publication/electronic-transactions-in-the-mozambican-legal-system)  
40. 25 Top MLOps Tools You Need to Know in 2025 \- DataCamp, accessed July 29, 2025, [https://www.datacamp.com/blog/top-mlops-tools](https://www.datacamp.com/blog/top-mlops-tools)  
41. 27 MLOps Tools for 2025: Key Features & Benefits \- lakeFS, accessed July 29, 2025, [https://lakefs.io/blog/mlops-tools/](https://lakefs.io/blog/mlops-tools/)  
42. 10 Open Source Tools for Building MLOps Pipelines \- Jozu, accessed July 29, 2025, [https://jozu.com/blog/10-open-source-tools-for-building-mlops-pipelines/](https://jozu.com/blog/10-open-source-tools-for-building-mlops-pipelines/)  
43. A curated list of awesome MLOps tools \- GitHub, accessed July 29, 2025, [https://github.com/kelvins/awesome-mlops](https://github.com/kelvins/awesome-mlops)  
44. Docker and Kubernetes for local deployment using FastAPI | by Andrew Wreford Eshakz, accessed July 29, 2025, [https://medium.com/@wrefordmessi/docker-and-kubernetes-for-local-deployment-using-fastapi-1c8df431ed95](https://medium.com/@wrefordmessi/docker-and-kubernetes-for-local-deployment-using-fastapi-1c8df431ed95)