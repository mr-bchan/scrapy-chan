import processor.db.helper as helper

rows = helper.get_posts(['*'], '*')

print(rows[0:100])
print('\n\ndone!')