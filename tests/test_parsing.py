import __init__

if __name__ == '__main__':
    from src.dgrm import convert_string_to_graph

    input_string = """TO["Task open"]
Reject["Reject"]
Rejected["Rejected"]
Close1["Close"]
NR["Need review"]
Reopen["Reopen"]
ORv["On review"]
Close2["Close"]
Closed["Closed"]
Start["Start"]
CE["Calculate estimate"]
SN["Send notification"]
End["End"]
###
TO --> Reject
Reject --> Rejected
TO --> Close1
Close1 --> NR
NR --> ORv::Yes
ORv --> Reopen
Reopen --> TO
ORv --> Close2
Close2 --> Closed
NR --> Closed::No
Closed --> Start::Close subprocess
Start --> CE
CE --> SN
SN --> End"""
    graph = convert_string_to_graph(input_string)
    graph.draw('diagram.png', prog='dot')
    assert graph.number_of_nodes() == 13
    assert graph.number_of_edges() == 14
