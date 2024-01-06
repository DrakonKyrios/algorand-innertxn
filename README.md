# Inner Transaction

### Algorand Starter Guide

> For initial guidance go to [Algorand Initial Startup Guide.](.algokit/README.md)

## Summary

Created this quick example of an Inner Transaction Application Call using a PyTeal Smart Contract created by the Beaker Framework CLI Tool.

## Purpose

With Algorand limited documentation and examples online, just wanted to put a proof of concept example out there of a simple smart contract that makes an application call to a global state smart contract. Also added pyTests to check for regression. The major call out that I was missing from my initial understanding is the settings of foreign apps on the root method transaction call that contains the inner transaction application call.

> [!NOTE]
> On my failed attempts I was trying to set the foreign apps property on the create or opt in calls

### Tasks

- [x] Create Inner Transaction Application Call that alters Global State
- [ ] Create Inner Transaction Application Calls that alters the local state of each account associated with the broker smart contract
