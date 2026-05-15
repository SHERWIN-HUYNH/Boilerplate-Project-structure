
**Fresh Graduate AI-Allowed Coding Test**

_Distributed Messaging Delivery Service_

**Goal:** Build a messaging delivery service that accepts large volumes of messages, processes them asynchronously, handles retries, and writes final delivery results to a file.

**Allowed languages:** Node.js, Golang, or Python.

**AI usage:** AI tools are allowed, but candidates must document how they used them and must understand all submitted code.

# 1\. Problem Statement

Design and implement a distributed messaging delivery service. The service receives messages from producers, queues them, processes them asynchronously, simulates delivery, retries temporary failures, and writes final results to an output file.

# 2\. Functional Requirements

## 2.1 Accept Messages

Provide an API or CLI to submit messages. Each message should include:

{

"message_id": "unique-id",

"recipient": "user-123",

"channel": "email | sms | push",

"priority": "high | normal | low",

"content": "message body",

"created_at": "timestamp"

}

## 2.2 Retry Logic

Temporary failures must be retried with backoff.

- Retry up to 3 times
- Increase delay after each retry
- Mark message as failed after max retries

## 2.3 Output Final Results to File

Every final delivery result must be written to an output file. Retry attempts should not create duplicate final rows.

Successful result example:

{

"message_id": "msg-001",

"recipient": "user-123",

"channel": "email",

"status": "delivered",

"attempts": 1,

"delivered_at": "timestamp"

}

Failed result example:

{

"message_id": "msg-002",

"recipient": "user-456",

"channel": "sms",

"status": "failed",

"reason": "max retries exceeded",

"attempts": 3,

"finished_at": "timestamp"

}

Output format can be JSONL, CSV, or plain text log.

# 3\. Technical Requirements

Candidates should implement:

- Message producer or API
- Queue or queue-like mechanism
- Worker service
- Retry mechanism
- Output writer
- Basic logging
- Basic metrics or counters
- README explaining design decisions


# 5\. Benchmark Requirement

The benchmark must run on a normal developer PC or laptop. No cloud infrastructure is required. The benchmark is focused on file-based final output only.

## 5.1 Minimum Benchmark Target

Candidates must prove that their system can complete:

Total messages: 1,000,000

Maximum completion time: 10 minutes

Output: final result file

This means the system should achieve at least:

Average processing throughput: approximately 1,667 messages/second

## 5.2 Benchmark Rules

- All final results must be written to file.
- The output file must contain exactly one final result per submitted message.
- Retry attempts should not create duplicate final output rows.
- The benchmark must include success, temporary failure, and permanent failure simulation.
- The benchmark must run from a clean start.
- The benchmark result must be reproducible using one command.

## 5.3 Required Benchmark Report

Candidates must include BENCHMARK.md with the following information:

Benchmark configuration:

\- Total messages: 1,000,000

\- Worker count:

\- Batch size:

\- Queue/storage approach:

\- Output file format:

Result:

\- Completed within 10 minutes: Yes/No

\- Total duration:

\- Messages completed:

\- Final output rows:

\- Average throughput:

\- Success count:

\- Failed count:

\- Retry count:

\- Duplicate final rows:

\- Data loss count:

# 6\. AI Usage Policy

AI tools are allowed. Candidates must include an AI_USAGE.md file describing:

- Which AI tool they used
- What prompts they used
- Which parts were AI-assisted
- What they reviewed or changed manually
- Any known limitations

Candidates are responsible for understanding all submitted code.

# 7\. Time Limit

- 2 hours