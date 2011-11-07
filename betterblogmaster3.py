import urllib, datetime, re, csv, pyblog, pprint
from datetime import datetime, timedelta

#
#  This is a very simple script that pulls the number of posts written from a series of wordpress blogs
#  It only checks last month's entries. It only checks ITKnowledgeExchange blogs.
#  It only works if there's an admin password with access, and if XML-RPC is enabled
#  -Michael Morisy, 2010

# Changelog:
# Nov. 3, 2010: The script mostly works now in telling you how many posts were posted in the previous month.
# Known Issues:
# - If the scope of "fetchedposts" doesn't stretch back enough to cover all posts written this month + all posts written last month,
# the script will give you bad data.
# - Doesn't count comments on posts.
# - Wrong password will tell you that all the blogs are configured improperly.

#important variables:
fetchedposts = 70 #how many blogs back to check. The higher it is, the slower it works, but the less likely it is to be tripped up by frequent posters.
pp = pprint.PrettyPrinter(indent=4)

pwd = raw_input("What is your password?")

csvfile=open('blogmasteroutput.csv','ab') #this is the excel-compatible file that the data is piped to.
csvout=csv.writer(csvfile,dialect='excel')


bloglist = file('bloglist.txt').readlines()
bloglist = [name.strip() for name in bloglist]

this_month_start = datetime.now().date().replace(day=1)
prev_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
print "We're looking for blog posts between " + str(prev_month_start) + " and " + str(this_month_start) + "."
print "Important caveat: We're only checking the " + str(fetchedposts) + " most recent posts. This number can be modified in the source code."
for blogurl in bloglist:
    try:
        url = 'http://itknowledgeexchange.techtarget.com' + blogurl + 'xmlrpc.php'
        blog = pyblog.WordPress(url, 'admin', pwd)
        posts = blog.get_recent_posts(numposts = fetchedposts)

        last_month_posts = [
            p for p in posts
                if prev_month_start <= datetime.strptime(str(p['dateCreated']), '%Y%m%dT%H:%M:%S').date() < this_month_start]
        last_month_approved_comment_count = 0
        #for p in posts:
        #    last_month_approved_comment_count = last_month_approved_comment_count + blog.get_comment_count(postid = p)['approved']
         # need to go in and re-add comment counts. Low priority.
        print "number of last month's posts at " + blogurl + ":", len(last_month_posts)
        print "number of approved comments for last month's " + str(blogurl) +" pages:",
        print last_month_approved_comment_count
        csvout.writerow([blogurl, len(last_month_posts), last_month_approved_comment_count])

    except pyblog.BlogError:
        print "Oops! The blog at " + blogurl + " is not configured properly."
        csvout.writerow([blogurl, "Error!", "Error!"])
                        

csvfile.close()