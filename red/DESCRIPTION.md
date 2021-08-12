# MVC-B developing model

this is like `MVC` model, contains a new part titled `Bot`:

```text
                                                .__________.       .__________.
                                         /~~~~> |Controller| ~~~~> |   Model  |
                                        /       |__________| <---- |__________|
                                       /             |
                                      /              V
.__________.       .__________.      /          .__________.
|   User   | ~~~~> |   Bot    | ~~~~/           |   View   |
|__________| <---- |__________| <-------------- |__________|
```

1. `User` is the telegram account sending some messages
2. `Bot` handles all message, commands, queries, etc.
3. `Controller` recieves the messages; proceses tasks.
4. `Model` works with database(s)
5. `View` catches data and send messages/events to user (using `Bot`)

## 3 rules

there are 3 important rules for all telegram messages:

1. just commands start any process.
2. queries continues any process.
3. each query can contain some data, in this form:

```text
<command_code>&<query_code>&<next_mode_index1>&<data>
```
