# Goal

Simple banking application model using Domain Driven Design.
The app accounts for authorization and management of accounts.
Accounts can perform transfers to other accounts.

# Context diagrams

- All value objects are immutable and do not contain identifiers.
- Value objects are represented with rounded-corner boxes and have underlined names.
- All entities and aggregate roots contain unique identifiers.
- Entities and aggregate roots are represented with sharp-corner boxes.
- All dates and datetimes are in UTC.

## Authorization context

```mermaid
flowchart TD
    classDef align_left text-align:left

    subgraph Account aggregate
        user[
            <b>User</b>
            <hr><u>authorization: Authorization</u>
            <u>email: Email</u>
            username: string
        ]:::align_left

        email(
            <b><u>Email</u></b>
            <hr>email: string
        ):::align_left

        auth(
            <b><u>Authorization</u></b>
            <hr>password hash: bytes
            password salt: bytes
        ):::align_left

        user --> auth
        user --> email
    end

    subgraph Session aggregation
        session[
            <b>Session</b>
            <hr><u>device: Device</u>
            started at: datetime
            expires at: datetime
            session token: bytes
            refresh token: bytes
        ]:::align_left

        device(
            <b><u>Device</u></b>
            <hr>IP address: bytes
            HTTP Agent: string
            HTTP Version: enum
        ):::align_left

        session --> device
    end

    user -- 1:n --- session
```

Property | Restriction
---|---
username | 1-63 characters, regex `^[a-zA-Z0-9 ]$`
email | 1-127 characters, regex `^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$`
password hash | 256 bytes
password salt | 256 bytes
started at | Less than `expires at`
expires at | Greater than `started at`, greater than now
session token | 512 bytes
refresh token | 512 bytes
IP address | 128 bytes
HTTP Agent | 0-255 characters
HTTP Version | `1.0`, `1.1`, `2.0` or `3.0`

## Account management context

```mermaid
flowchart TD
    classDef align_left text-align:left

    subgraph Account management aggregate
        user[
            <b>User</b>
            <hr><u>contact: Contact</u>
            <u>personal: Personal</u>
        ]:::align_left

        contact(
            <b><u>Contact</u></b>
            <hr><u>email: Email</u>
            <u>telephone: Telephone</u>
            <u>address: Address</u>
        ):::align_left

        email(
            <b><u>Email</u></b>
            <hr>email: string
        ):::align_left

        phone(
            <b><u>Telephone</u></b>
            <hr>country prefix: enum
            telephone number: string
        ):::align_left

        address(
            <b><u>Address</u></b>
            <hr>country: enum
            zip code: string
            city: string
            street name: string
            street number 1: string
            street number 2: string
        ):::align_left

        personal(
            <b><u>Personal</u></b>
            <hr>first name: string
            second name: string
            surname: string
            date of birth: date
            sex: enum
        ):::align_left

        account[
            <b>Account</b>
            <hr>account number: string
            account name: string
            account type: enum
            account locked: bool
        ]:::align_left


        user --> contact
        contact --> address
        contact --> phone
        contact --> email
        user --> personal
        user -- 1:n --> account
    end
```

Property | Restriction
---|---
email | 1-127 characters, regex `^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$`
country prefix | Enum of country prefixes
telephone number | 9 characters, regex `^[0-9]{9}$`
country | Enum of countries
zip code | 5 characters, regex `^[0-9]{5}$`
city | 1-255 characters, regex `^[a-zA-Z ]{1, 255}$`
street name | 1-255 characters, regex `^[a-zA-Z ]{1, 255}$`
street number 1 | 1-255 characters, regex `^[a-zA-Z0-9 ]{1, 255}$`
street number 2 | 0-255 characters, regex `^[a-zA-Z0-9 ]{0, 255}$`
first name | 1-255 characters, regex `^[a-zA-Z]{1, 255}$`
second name | 0-255 characters, regex `^[a-zA-Z ]{0, 255}$`
surname | 1-255 characters, regex `^[a-zA-Z]{1, 255}$`
sex | `male`, `female` or `other`
account number | 17 characters, regex `^[0-9]{17}$`
account name | 1-63 characters, regex `^[a-zA-Z0-9 ]{1, 63}$`
account type | `Checking`, `Savings`, etc.



## Transfer context

```mermaid
flowchart TD
    classDef align_left text-align:left

    subgraph Transfer aggregate
        transfer[
            <b>Transfer</b>
            <hr>from: Account
            to: Account
            amount: integer
            requested at: datetime
            completed at: datetime?
        ]:::align_left

        account[
            <b>Account</b>
            <hr>account number: string
            account locked: bool
            saldo: integer
        ]:::align_left

        transfer -- 1:2 --> account
    end
```

Property | Restriction
---|---
amount | Positive integer
completed at | Optional, greater than `requested at`
account number | 17 characters, regex `^[0-9]{17}$`
saldo | Non-negative integer
