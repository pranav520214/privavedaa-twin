# Research boundaries

## Simple explanation
This is a virtual research laboratory, not a treatment tool.

## Technical explanation
Public computations use server-generated synthetic records. Output schemas carry the
research label. No optimization objective or patient dosing endpoint is implemented.
Text screening is defense in depth, not a complete detector of clinical advice.

## Why we need it
A concentration curve or ranked observation can easily be mistaken for a medical instruction.

## Implementation
Every page displays RESEARCH SIMULATION — NOT FOR CLINICAL DECISION-MAKING.
Information results are labeled MODEL INFORMATION VALUE. Scenarios use neutral identifiers.
Storage excludes names, contact data and other unnecessary identifiers.
The local development API must bind to loopback; it is not an authenticated multiuser service.

## Tests
Check labels and forbidden language across response objects and dashboard pages;
reject non-synthetic inputs, nonfinite numbers and unreviewed extraction candidates.
