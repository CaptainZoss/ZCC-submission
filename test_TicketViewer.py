import unittest
import random
import TicketViewer

class test_TicketViewer (unittest.TestCase):
    
    def test_get_tickets_success (self): 
        credentials = ("amanzewge@gmail.com/token", "uz6m4OJel6Yk7pVi9RYu8tPLStEDCGkSp9VlRZfg")
        endpoint = "https://zccaman.zendesk.com/api/v2/tickets"
        result = TicketViewer.get_tickets(endpoint, credentials) 
        self.assertIsInstance (result[0], list)
        self.assertIsInstance (result[1], int)
    
    def test_get_tickets_fail (self):
        credentials = ("fakename.com/token", "uz6m4OJel6Yk7pVi9RYu8tPLStEDCGkSp9VlRZfg")
        endpoint = "https://zccaman.zendesk.com/api/v2/tickets"
        result = TicketViewer.get_tickets(endpoint, credentials) 
        print (result)
        self.assertIsNone (result[0])
        self.assertIsNone (result[1])
    
    def test_display_tickets_success (self):
        credentials = ("amanzewge@gmail.com/token", "uz6m4OJel6Yk7pVi9RYu8tPLStEDCGkSp9VlRZfg")
        endpoint = "https://zccaman.zendesk.com/api/v2/tickets"
        tickets, n = TicketViewer.get_tickets(endpoint, credentials) 
        if (n%25 == 0):
            total_pages = n/25
        else:
            total_pages = (n//25) + 1
        
        page = random.choice(range(1, total_pages)) #pick a random page
        startID =  (page - 1) * 25 + 1
        endID = min(startID + 24, len(tickets))
        result = TicketViewer.display_tickets(tickets, n, total_pages, page)
        self.assertEqual(result[0] , startID)
        self.assertEqual(result[1] , endID)
    
    def test_display_tickets_fail (self):
        tickets = [] 
        n = 5 
        total_pages = 1
        page = 2 
        startID =  (page - 1) * 25 + 1
        endID = min(startID + 24, len(tickets))
        result = TicketViewer.display_tickets(tickets, n, total_pages, page)
        self.assertEqual(result , None)
    
    def test_display_one_ticket_success(self):
        credentials = ("amanzewge@gmail.com/token", "uz6m4OJel6Yk7pVi9RYu8tPLStEDCGkSp9VlRZfg")
        endpoint = "https://zccaman.zendesk.com/api/v2/tickets"
        tickets, n = TicketViewer.get_tickets(endpoint, credentials) 
        result = TicketViewer.display_one_ticket(tickets, 0) 
        self.assertEqual(result["id"] , 1)

    def test_display_one_ticket_fail(self):
        credentials = ("amanzewge@gmail.com/token", "uz6m4OJel6Yk7pVi9RYu8tPLStEDCGkSp9VlRZfg")
        endpoint = "https://zccaman.zendesk.com/api/v2/tickets"
        tickets, n = TicketViewer.get_tickets(endpoint, credentials) 
        result = TicketViewer.display_one_ticket(tickets, 200) 
        self.assertEqual(result , None)

if __name__ == '__main__':
    unittest.main()