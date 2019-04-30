good example:
re.findall('(work|job)(.*?)(?=work|job|$)', STRING, flags=re.S)  -> by this method, you can find all 'work&job' even if it's out-of-order in one line
re.sub('^([^\n]+[^\n:£º])\n', r'\1:\n', STRING)  -> by this method, you can find the first line that ends without ':or£º', then by r'\1' get the original str, do next thing you want


Five Basic Methods Of Function
re.match(reRule, string, flags)  -> just once match
re.search(reRule, string, flags)  -> just once match
re.findall(reRule, string, flags)  -> just once match
re.sub(reRule, replaceStr, string, flags)
re.split(reRule, string)

()  -> meaning match a string of characters, then store them in a group
[]  -> meaning match anything in it once, [a-z] is matching a->b, if you don't want to match, you can add [^] to not match
{}  -> meaning match times you appoint, such as \d{2, 9}, that is match two nums -> nine nums

*  -> {0, }
+  -> {1, }
?  -> {0, 1}

(?<=)  -> meaning match start with it
(?<!)  -> meaning match not start with it
(?=)  -> meaning match ends with it
(?!)  -> meaning match not ends with it
(?:)  -> match bu not store, that to say don't make a group

