## The Supply Chain Beergame
A basic python implementation

## What is this? 
The "Beergame" is a game supply chain nerds typically play at some point while in school or at a conference. It simulates the bullwhip effect in logistics and is meant as an educational tool. The premise of the game is that you manage one of four different roles in a beer supply chain (thus the beer game). As such, you are trying to make the most amount of money for your business by having the least amount of holding (the cost of keeping something in a warehouse for any amount of time) and backorder costs (the cost of not being able to fulfil a sale) possible. Easy peasy! 

### The Rules
- There are 4 players - Retailer, Supplier, Distributor, and Manufacturer. 
    - Each player sits up or down stream from another player: Manufacturer makes the beer and sends it to the distributor who sends it to the supplier who sends it to the retailer who sells it to the customer. 
- There are N number of rounds (20 is the default in this example). 
- Every round a player ships inventory to meet their demand and makes an order to restock.
    - The catch: it takes a week for the upstream player to get your order and it takes a week for them to ship it to you.
- If a player keeps inventory on hand they must pay the holding cost for that inventory and if they can't ship a order on time because they don't have enough inventory they pay a backorder cost. The goal of the game is to minimize these costs. 

## Why? 
This game illustrates a concept that is import not only for supply chain nerds to understand but also for consumers, like you and me, to understand how our demand signaling can have a big impact on what products are available and when. In today's world a lot is made of shortages in supply chains due to the pandemic and other factors, playing this game will not make someone an expert in supply chains but it will help people gain some understanding of what needs to happen for you to get your beer where and when you want it! 

## Web Component: in construction 
`docker-compose up --build` should get you going if you want to add a UI layer. 

