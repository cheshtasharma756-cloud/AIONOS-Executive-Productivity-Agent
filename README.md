# Executive Productivity Agent

## AIONOS Assignment 1

An agent-style Executive Productivity Assistant that converts messy executive inputs such as emails, meeting notes, calendar information, and voice-note reminders into a structured daily action brief.

**Executive:** Arjun Malhotra  
**Role:** VP Sales  
**Assignment:** Executive Productivity Agent

---

## 1. Problem Statement

Executives receive information from multiple sources such as emails, meetings, calendar events, and personal reminders.

Important commitments can be repeated, changed, completed, or left with unclear ownership.

The goal of this prototype is to transform these fragmented inputs into a concise and actionable executive brief.

The agent focuses on:

- Identifying commitments and actions
- Separating the executive's own actions from actions waiting on others
- Detecting deadlines and overdue items
- Deduplicating repeated mentions of the same action
- Detecting unclear ownership without making assumptions
- Providing a daily executive brief
- Answering questions about commitments and tasks

---

## 2. Data Sources

The prototype uses the supplied AIONOS Assignment 1 data pack.

The input information is based on:

- Leadership Sync / meeting notes
- Email threads
- Calendar information
- Voice-note reminders

The prototype uses only the information provided in the assignment data pack and does not invent missing facts.

---

## 3. Processing Pipeline

The agent follows the following workflow:

```text
Messy Executive Inputs
        ↓
Extract
        ↓
Resolve
        ↓
Deduplicate
        ↓
Validate
        ↓
Executive Productivity Agent
        ↓
Daily Brief / Action Views / Ask Agent


### Processing Stages

**Extract**

Identify actions, commitments, deadlines, people, and status information from the supplied inputs.

**Resolve**

Determine the relevant owner, requester, deadline, and current status.

**Deduplicate**

Combine repeated mentions of the same underlying action into a single action item.

**Validate**

Check for ambiguity and avoid inventing information when ownership or other details are unclear.

**Brief**
 Present the processed information in an executive-friendly format. 

 ---

## 4. Key Capabilities

### My Actions

Shows actions that require Arjun's attention.

Example:
- Send the updated vendor list to Raghav
- Latest commitment: Wednesday morning

### Waiting / Scheduled

Shows actions or events that are scheduled or depend on other people.

Examples:
- Meridian Logistics client call
- Q3 campaign deck review

### Unclear Ownership

The agent explicitly flags actions where ownership is not confirmed.

Example:
- Mumbai office lease renewal
- Deadline: Friday EOD
- Owner: UNCONFIRMED

The agent does not assume that Facilities owns the action simply because Facilities is involved in the discussion.

### Completed

Shows actions that have already been completed.

Example:
- July expense variance report

### Ask Agent

The user can ask natural-language questions about the executive's actions and commitments.

Example questions:
- What did I promise Raghav?
- What needs action today?
- What is the status of the Mumbai office lease?
- What is the vendor list deadline?
- What happened with the Meridian call?

---

## 5. Deduplication Example

The vendor-list commitment appears multiple times across the email thread.

Instead of treating each email as a separate task, the agent identifies them as updates to the same underlying commitment.

The result is one consolidated action:

**Action:** Send updated vendor list to Raghav  
**Owner:** Arjun  
**Latest deadline:** Wednesday morning  
**Status:** My Action

This prevents repeated email mentions from creating duplicate tasks.

---

## 6. Ambiguity Handling

A key edge case is the Mumbai office lease renewal.

The source material indicates:
- The lease renewal requires an authorized signature.
- Facilities is involved in the discussion.
- Ownership is not explicitly confirmed.
- The deadline is Friday EOD.

Therefore, the agent marks:

**Owner: UNCONFIRMED**

The system does not infer ownership from context when the source material does not explicitly establish it.

This is important because an incorrect action owner can create misleading executive actions.

---

## 7. Current Action Summary

The prototype currently organizes the supplied assignment data into:

| Action | Owner | Status | Deadline |
|---|---|---|---|
| Send updated vendor list | Arjun | My Action | Wednesday morning |
| Confirm Mumbai lease ownership | Unconfirmed | Unclear Ownership | Friday EOD |
| Meridian Logistics client call | Arjun | Scheduled | Wednesday 3 PM |
| Review Q3 campaign deck | Arjun | Scheduled | Thursday 9:30 AM |
| Review July expense variance | Arjun | Completed | Wednesday evening |

---

## 8. Technology

- Python
- Streamlit
- Source-grounded processing
- Rule-based action classification
- Natural-language question handling
- Structured action representation

The prototype is intentionally lightweight so that the core executive-productivity workflow remains easy to understand, test, and demonstrate.

---

## 9. Project Structure

```text
AIONOS_Executive_Agent/
│
├── app.py
├── requirements.txt
├── README.md
|── .gitignore
