package event

import (
	"time"
)

type Event struct {
	EventDescription string
	EventDate        time.Time
}

var HolidayMaps = []map[string]*Event{
	//EVENTS for Chennai outlet
	{
		"Pongal Festival": &Event{
			EventDescription: "The Pongal festival in Chennai brings increased shopping activity. We anticipate higher demand for traditional wear like cotton dresses and ethnic tops. T-shirts with traditional prints are also popular during this season.",
			EventDate:        time.Date(2024, 1, 15, 0, 0, 0, 0, time.UTC),
		},
		"Summer Fashion Week": &Event{
			EventDescription: "Chennai Summer Fashion Week attracts fashion enthusiasts. Expect increased demand for trendy tops and summer dresses. Light fabric t-shirts and comfortable pants are essential for the warm weather.",
			EventDate:        time.Date(2024, 4, 15, 0, 0, 0, 0, time.UTC),
		},
		"Diwali Shopping Season": &Event{
			EventDescription: "The Diwali shopping season sees peak retail activity. Traditional wear and festive clothing collections should be stocked up. Premium dresses and designer tops are in high demand.",
			EventDate:        time.Date(2023, 11, 12, 0, 0, 0, 0, time.UTC),
		},
		"College Season Start": &Event{
			EventDescription: "Beginning of college semester brings young shoppers. Casual t-shirts, trendy tops, and comfortable pants are essential. Stock up on student-friendly fashion items.",
			EventDate:        time.Date(2024, 6, 1, 0, 0, 0, 0, time.UTC),
		},
	},
	//EVENTS for Bangalore outlet
	{
		"Tech Fashion Expo": &Event{
			EventDescription: "Bangalore's Tech Fashion Expo combines technology and fashion. Modern corporate wear including formal pants and tops are in demand. Smart casual t-shirts popular among tech professionals.",
			EventDate:        time.Date(2024, 2, 15, 0, 0, 0, 0, time.UTC),
		},
		"Monsoon Sale": &Event{
			EventDescription: "The monsoon season requires weather-appropriate clothing. Water-resistant materials and practical fashion items should be stocked. Casual wear and rain-friendly clothing see increased demand.",
			EventDate:        time.Date(2024, 7, 1, 0, 0, 0, 0, time.UTC),
		},
		"Corporate Fashion Week": &Event{
			EventDescription: "Bangalore's corporate fashion week targets office wear. Formal dresses, business casual tops, and professional pants are essential. Premium formal wear collections should be increased.",
			EventDate:        time.Date(2024, 3, 10, 0, 0, 0, 0, time.UTC),
		},
	},
	//EVENTS for Mumbai outlet
	{
		"Bollywood Fashion Show": &Event{
			EventDescription: "Mumbai's Bollywood Fashion Show influences local fashion trends. Designer dresses and celebrity-inspired clothing lines see peak demand. Trendy tops and fashionable pants are essential.",
			EventDate:        time.Date(2024, 5, 15, 0, 0, 0, 0, time.UTC),
		},
		"Mumbai Fashion Street Festival": &Event{
			EventDescription: "The street fashion festival celebrates urban style. Casual t-shirts, street-wear collections, and trendy tops are in high demand. Youth-focused fashion items should be well-stocked.",
			EventDate:        time.Date(2024, 8, 1, 0, 0, 0, 0, time.UTC),
		},
		"Wedding Season Special": &Event{
			EventDescription: "Wedding season brings demand for formal and party wear. Designer dresses and premium formal wear see increased sales. Formal tops and elegant pants collections should be expanded.",
			EventDate:        time.Date(2024, 11, 20, 0, 0, 0, 0, time.UTC),
		},
	},
	//EVENTS for Pune outlet
	{
		"College Fashion Week": &Event{
			EventDescription: "Pune's college fashion week targets young fashion enthusiasts. Casual t-shirts, trendy tops, and comfortable pants are essential. Youth-oriented fashion collections should be increased.",
			EventDate:        time.Date(2024, 7, 15, 0, 0, 0, 0, time.UTC),
		},
		"Winter Collection Launch": &Event{
			EventDescription: "Winter fashion launch event in Pune. Warm clothing including long-sleeve tops and winter wear collection. Seasonal fashion items should be well-stocked.",
			EventDate:        time.Date(2023, 12, 1, 0, 0, 0, 0, time.UTC),
		},
		"Cultural Fashion Festival": &Event{
			EventDescription: "Pune's cultural festival combines traditional and modern fashion. Fusion wear including modern dresses and ethnic-inspired tops are popular. Contemporary fashion with traditional elements sees high demand.",
			EventDate:        time.Date(2024, 9, 5, 0, 0, 0, 0, time.UTC),
		},
	},
}
