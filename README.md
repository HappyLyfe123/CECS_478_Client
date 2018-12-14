# CECS_478_Client
The purpose of the client is to encrypt and decrypt messages send between user.

## Table of Contents
1. [Time Allocation](#time%201%20allocation)
2. [Requirements](#Requirements)
3. [Architecture](#Architecture)

## Time Allocations
10 Hours Server and Client Design
24 Hours Server and Client implmentation
6 Hours Documentation

## Requirements
1. Python 3

### Frontend Framework of Choice
Python 3
The reason why we chose Python 3 to develop our client becuase it have a wide community support. It also have a lot of libaries 
that help speed up the development process.

### Security
AES Encryption
The reason why we use AES for encryption becasue it's the insudtry standard for encryption

HMAC
We use HMAC for message integrity. This allows us to check if the message had been alter in anyway during transit.

RSA Key Exchange
The reason why we use RSA becuase we need a way to encrypt AES and HAMC key when we send it with the message.
