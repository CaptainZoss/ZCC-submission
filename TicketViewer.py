import requests
from prettytable import PrettyTable
import time

def get_tickets(endpoint, credentials):
        r = requests.get(endpoint, auth= credentials) #connect using api key
        if (not r.ok): #if API is unavailable
            print ("Error connecting to API. Please try again later.")
            return (None, None)

        d = r.json() #convert response to python dictionary
        tickets = d["tickets"]
        count = d["count"]

        if (d["next_page"]):# if there is a next page fetch the tickets from it
            return (tickets + get_tickets(d["next_page"], credentials)[0], count)
        
        return (tickets, count)

def display_tickets(tickets, n, total_pages, page = 1):# displays the tickets and other information such as page numbers and number of tickets
    if (not page in range (1, total_pages+1)): return None 
    t = PrettyTable() #create new table
    t.title = "Tickets"
    t.field_names = ["ID", "Created at", "Subject", "Status"]
    offset = 25*(page - 1) #used to access tickets from other pages by ofsetting the indexes based on page number
    for i in range(25):
        if i + offset in range(len(tickets)):
            item = tickets[i + offset]
            t.add_row ([str(item["id"]) , item["created_at"] , item["subject"] , item["status"]])
        else: 
            i = i-1 #save the index of the final item
            break
    print(t)
    print ( "Page: " + str(page) + "/" + str(total_pages) + "\n" +str((page-1)*25 + 1) + "-" + str(i+offset+1) + " of " + str(n) + " tickets") 
    return ((page-1)*25 + 1, i+offset+1) #return range of printed tickets for unit testing 
    
def display_one_ticket(tickets, n): #displays one ticket with the given index
    if (n) in range (len(tickets)): 
        ticket = tickets[n]
        t = PrettyTable() #table to hold out ticket information
        t.title = "Ticket information"
        t.field_names = ["ID", "Created at", "Updated at", "Priority" ,  "Subject", "Status"]
        t.add_row ([str(ticket["id"]) , ticket["created_at"], ticket["updated_at"] , ticket["priority"] , ticket["subject"] , ticket["status"]])
        print(t)
        print ("\nDesciption: \n\n" + ticket["description"] + "\n")
        return ticket
    else: print("No Ticket with that ID number")


def run(): # the main loop of the program
    credentials = ("amanzewge@gmail.com/token", "uz6m4OJel6Yk7pVi9RYu8tPLStEDCGkSp9VlRZfg")
    endpoint = "https://zccaman.zendesk.com/api/v2/tickets"
    tickets = []
    page = 0 #tracks which page we are looking at
    n = 0 #tracks the total number of tickets
    total_pages = 0 #the total number of pages using the 25 tickets per page rule
    print ("Welcome to the Ticket Viewer!")
    
    #create instructions table
    instuctions = PrettyTable()
    instuctions.title = "Commands"
    instuctions.field_names = ["Key", "Action"]
    instuctions.add_row (["a", "View All tickets"])
    instuctions.add_row (["any digit", "View Ticket with that ID"])
    instuctions.add_row (["n", "Go to Next page"])
    instuctions.add_row (["p", "Go to Previous page"])
    instuctions.add_row (["c", "View commands"])
    instuctions.add_row (["q", "Quit program"])
    print(instuctions)


    tickets, n = get_tickets(endpoint, credentials)#get the tickets and the number of tickets from the API

    if tickets == None: #error retreiving the tickets
        while True:
            val = input('Press "r" to try again or "q" to quit > ')
            if val == "r":
               return run()
            elif val == "q": quit()

    #calculate the total number of pages based on the 25 per page rule
    if (n%25 == 0):
        total_pages = n/25
    else:
        total_pages = (n//25) + 1

    while True:
        val = input('Press "c" to view commands > ') 
        if val == "a":
            if (page == 0): page = 1
            display_tickets(tickets, n, total_pages, page)
        elif val == "n": # next page
            if page == 0: print ('Press "a" to bring up the tickets first')
            elif page < total_pages: 
                page += 1
                display_tickets(tickets, n, total_pages, page) 
        elif val == "p": #previous page
            if page == 0: print ('Press "a" to bring up the tickets first')
            elif page > 1: 
                page -= 1
                display_tickets(tickets, n, total_pages, page) 
        elif val == "q": #quit
            print ("Thank you for using TicketViewer!")
            time.sleep(2)
            quit()
        elif val.isdigit():
            display_one_ticket(tickets, int (val) - 1)    # val -1 because list index starts at 0 but id's start at 1        
                
        elif val == "c":print(instuctions)
        else: print ("Invalid command")


if __name__ == '__main__':
    run()
