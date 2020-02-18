## Log Analytics : GS Quantify 2019
Problem Statement : Identifying the intent of each log line and group log lines with the same intent in the same cluster.

### Context
Companies depends upon logs to monitor the behavior of thousands of applications which process millions of trades, helps manage risk, support algorithmic trading and so on. In all, these applications generate hundreds of millions of log lines every day which engineers comb through to identify and rectify application failures.
              However, different applications built by different engineers tend to communicate the same kinds of failures in different ways.This makes the process of identifying similar failures across different applications difficult and tedious.
The problem to solve is just this - given a set of log lines, assign each to a cluster. The overall goal of this problem is to identify the intent of each log line and group log lines with the same intent in the same cluster.

### Flow Diagram

![img](https://imgur.com/4iObT18.png)
