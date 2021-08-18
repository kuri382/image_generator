import pandas as pd

message_df = pd.read_csv("src/messages.csv")
print(message_df.iat[0,3])

word = "test"
next_word = "flas"
summary = "[REC_PRIVATE]test,dfadjkflsasdoa"
test = ["[REC]", "[REC_PRIVATE]"]
print(word in summary or next_word in summary)

print(any(map(summary.__contains__, (test))))