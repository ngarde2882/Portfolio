f = open("Desktop/reviews.txt", errors="ignore")
o = open("Desktop/reviews_outfile.csv", 'w')
skip = f.readline()
skip = f.readline()
o.write('Date,Rating,Cust_FirtsName,Cust_LastName,#Reviews,#Photos,Professionalism,Punctuality,Quality,Responsiveness,Value,Review\n')
i = 3
while i<14:
    ctx = f.readline()
    lst = ctx.split("fIQYlf")
    for x in lst[1:]:
        name = x.split('</a></div></div>')[0].split('>')[-1]
        date = x.split("dehysf lTi8oc\">")[1].split('</span')[0]
        rating = x.split('Rated ')[1].split(' out of 5')[0]
        try:
            revs = int(x.split("A503be\">")[1].split(' review')[0])
            try:
                photos = x.split('·</span>')[1].split(' pho')[0]
            except:
                photos = None
        except:
            try:
                revs = x.split('·</span>')[1].split(' rev')[0]
                try:
                    photos = x.split('·</span>')[2].split(' pho')[0]
                except:
                    photos = None
            except:
                revs = None
                photos = None
        try:
            cimzz = x.split('CimZZ\">')[1].split(':')[0]
            traits = x.split('PVxqTb\">&nbsp;<span>')[1:]
            j = 0
            while j<len(traits):
                traits[j] = traits[j].split('</span')[0]
                j+=1
        except:
            cimzz = None
            traits = None
        try:
            txt = x.split('<span class="review-full-text" style="display:none">')[1].split('<')[0]
            txt = txt.replace(',','')
            txt = txt.replace('â€™','\'')
            txt = txt.replace('â€','\"')
        except:
            try:
                txt = x.split('<span data-expandable-section="" tabindex="-1">')[1].split('<')[0]
                txt = txt.replace(',','')
                txt = txt.replace('â€™','\'')
                txt = txt.replace('â€','\"')
            except:
                txt = None
        print(f'{name},{rating},{date},{revs} reviews,{photos} photos,{cimzz}:{traits},{txt}')
        name = name.replace(',','')
        fname = name.split(' ')[0]
        try:
            lname = name.split(' ',1)[1]
        except:
            lname = ''
        o.write(f'{date},{rating},{fname},{lname},{revs},{photos},')
        if traits == None:
            o.write(f',,,,,{txt}\n')
        else:
            if 'Professionalism' in traits:
                o.write(f'{cimzz},')
            else:
                o.write(f',')
            if 'Punctuality' in traits:
                o.write(f'{cimzz},')
            else:
                o.write(f',')
            if 'Quality' in traits:
                o.write(f'{cimzz},')
            else:
                o.write(f',')
            if 'Responsiveness' in traits:
                o.write(f'{cimzz},')
            else:
                o.write(f',')
            if 'Value' in traits:
                o.write(f'{cimzz},{txt}\n')
            else:
                o.write(f',{txt}\n')
    i+=1
f.close()
o.close()