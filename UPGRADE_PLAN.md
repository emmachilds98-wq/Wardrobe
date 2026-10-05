# Dave's Wardrobe: review and upgrade plan

The live version is the claude.ai artifact
<https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2>. This folder is a backup of
it, so the page and its data can be used or rebuilt outside Claude.

| File | What it is |
|---|---|
| `page.html` | The page source as published (version 13, 5 Oct 2026). |
| `data/items.json` | All 964 picks, keyed by id, as stored in the artifact's `items` collection. |
| `data/outfits.json` | All 156 outfits from the `outfits` collection. |
| `tools/fetch_photos.py` | Downloads listing photos and packs them for the page (step 2 below). |

The shared shortlist, Dave's thumbs and saved outfits (`saved`, `votes`,
`myfits`) are not copied here. They change from day to day and belong to the
people using the page.

---

## 1. Review of the current helper (before this round)

**Works well**
- Seven styles (Classic, Casual, Street, Minimal, Rave, Outdoors, Lounge). Each one has its own
  guidance on colours, what to wear, what to avoid and where to spend.
- Outfits are drawn on a figure of Dave, and each piece is numbered, priced and linked. Running
  totals show the saving against full price.
- The builder has slots, a colour for each piece and a "suggest under £X" search. The
  "one piece, many outfits" view shows cost per wear.
- The shortlist is shared and tracks what has been bought, and Dave's thumbs feed back into the
  ranking.
- The size data is honest: an "in his size" line where the shop shows stock, and his usual size
  where it doesn't.

**Gaps found**
1. **No product photos.** Every card was text only, and the drawings were the only visuals. The
   artifact sandbox blocks images from shop websites, so photos cannot simply be hotlinked. They
   have to be downloaded and published with the page.
2. **Shop coverage was uneven.** About 48 shops had picks, but nearly half the picks were from
   ASOS, M&S or Uniqlo. Many shops in the "Where to look" directory (Arket, COS, Gap, Joules,
   FatFace, Loake, Dr Martens, Gymshark, Decathlon and others) had no picks at all.
3. **No supermarket or value tier.** Tu, George and F&F are some of the best value for basics
   and knitwear, and none of them were covered.
4. **"New this week" is busy.** Over 200 picks carry `added: 2026-10-05`. That is right for a
   big refresh, but the weekly refresh should only set `added` on picks that are actually new, or
   the New filter stops meaning much.
5. **Sizes are still estimates.** The shirt collar and jacket chest are marked "to confirm". Until
   Dave is measured, "in his size" is only as good as the guess.
6. **Some pages are near their load limit.** Picks load as two queries of up to 1,000 each
   (clothes: 466, everything else: 315). That leaves room for about 500 more clothes picks before
   the split needs a third query.

## 2. Done in this round (5 Oct 2026)

- **Photo support in the page.** Each pick card now has a picture area at the top. Outfit rows,
  the builder list and the shortlist get a thumbnail for each piece.
  - The page shows the listing photo when one is stored: an item's `img` field, or an entry in a
    photo pack named by the `meta/photos` document.
  - When there is no photo, or a photo fails to load, the card shows a drawing of the garment in
    its colour.
  - Cards with a real photo are labelled "Shop photo", and the footer explains the difference.
- **36 new picks from 20 shops that had no picks before:** Arket, COS, Hawes & Curtis, Loake
  (factory outlet), Jean Store (Dr Martens), Seasalt, Decathlon, FatFace, Joules, Zalando (New
  Balance, BDG), Office (Vans), Gymshark, Tu at Sainsbury's, George at Asda, Rohan, Summits
  (Berghaus), White Stuff and Stuarts London (Timberland).
  - Picks span all seven styles, from a £9.99 Decathlon fleece to £169 Dr Martens.
  - Each pick has a real listing link and the date its price was seen. Some prices are from
    May to August, and the card shows that date.
- **11 new outfits**, mostly built from the new picks:
  - The supermarket upgrade, Coastal weekend, Three-in-one walk, Docs and black denim, Old Skool
    Saturday, Quarter-zip pub
  - Film night, Charcoal and navy, Wet weekend, Green cord and navy, and About £100, all new
- **"Where to look" directory:** grew from 89 to 104 shops. Two new groups were added:
  "Supermarkets and value" and "Big multi-brand shops". Counts now show for the new shops.
- Totals: **781 picks, 105 outfits, 66 shops with picks.**

## 2b. Done in round two (5 Oct 2026, later)

- **Shop filter** in Picks. It lists the shops with picks in the current style or search, busiest
  first, with counts.
- **Compact grid** toggle in Picks. It shows a denser grid with picture, name, price and shop,
  for browsing on a phone. Each viewer's choice is remembered on their own device.
- **Price-drop watch on the shortlist.** Saving a pick now stores its price, and the shortlist
  shows "Down £X since it was saved" when the price falls. This only covers picks saved from now
  on.
- **Old-price warning.** Cards whose price was last seen more than 30 days before the latest
  check say so, in amber, with "Check before buying".
- **13 more picks from 8 more shops:** Zara, The North Face, Peregrine, Mountain Warehouse,
  Converse, Foot Locker (New Balance 740), Sports Direct (£11 windbreaker) and END. (YMC), plus
  Next.
- **5 more outfits:** Black bomber, white tee; Made in England; Cold festival queue; Warehouse
  night under £100; Chucks and black denim.
- Totals: **794 picks, 110 outfits, 74 shops with picks.**

## 2c. Photos (5 Oct 2026, evening)

- Network access was opened, and `fetch_photos.py --browser` ran over every pick.
- **483 of 794 picks now show the shop's own listing photo** (version 8 of the page, two packs
  of about 3.9 MB in total, roughly 8 KB per photo).
  - Every Uniqlo pick has a photo, and 118 of 120 from M&S.
  - The photos also show as thumbnails in outfits, the builder, the shortlist, "This week" and
    "One piece, many outfits".
- **Still drawings:**
  - ASOS (195 picks): it stalls every connection from cloud servers.
  - Pre-owned searches: they have no single photo.
  - Picks linking to brand or category pages (most M and M Direct ones).
  - Shops that block even a headless browser: Arket, COS, Zara (mostly), Next, Joules,
    The North Face, Converse, Decathlon, Adidas, Office, Zalando, H&M, Hawes & Curtis,
    John Lewis and a few others.
- 42 photos that several picks shared were dropped, because a shared photo is a shop logo or
  banner rather than the product.
- To fill the gaps, run the tool from a home computer: shops rarely block home broadband the way
  they block cloud servers. Then republish the packs.

## 2d. Round three: live stock (5 Oct 2026, evening)

- With network access, picks now come straight from shops' own product feeds
  (`tools/shopify_pull.py` downloads a shop's whole catalogue). Each new pick has:
  - the live price and full price
  - **real stock in his size** (L, 34W 32L or UK 11)
  - the shop's own photo
- **49 new picks**, all in stock in his size when checked:
  - Jean Store: Levi's 501, 578 and 568, Lee, Stan Ray, Carhartt WIP, Fred Perry and
    Colorful Standard.
  - Community Clothing, Uskees, Brakeburn, Farah, Lyle & Scott, Peregrine, Base London, Savile Row
    Company, Montirex, Cernucci, Original Penguin and Route One.
  - New shops: Finisterre and Albam.
  - Most are 40 to 70% off.
- **10 new outfits** built on them: 501s and a chore jacket, Made in Britain knit, Baggy 578s and
  a coach jacket, Workwear weekend, Cold Saturday in cord, Black utility, Merino and derbies,
  Parka and checks, Navy bomber with ecru denim, and Sofa, brown and navy.
- Totals: **843 picks, 120 outfits, 76 shops; 532 picks with the shop's photo.**
- Shops whose feeds work, for the weekly refresh: Jean Store, Route One, Community Clothing,
  Uskees, Brakeburn, Cernucci, Montirex, Herring, Savile Row Company, T.M. Lewin, Fila, Summits,
  Albam, Sunspel, Finisterre, Colorful Standard, Base London, Farah, Original Penguin, Lyle & Scott,
  Peregrine and Oliver Spencer.

## 2e. Done in round four (5 Oct 2026, night)

- **Data fixes.**
  - The two dead M&S dressing-gown links now point to live gowns (Fleece Supersoft, midnight navy,
    £35, and Pure Cotton Polka Dot, navy, £35).
  - Five picks with no style got one.
  - Prices re-checked where the shop allows it: Seasalt, END. (YMC, now £74), White Stuff and
    Peregrine.
  - Three picks removed: two Gymshark links that are gone, and a Berghaus fleece that sold out.
    The outfit that used the fleece now uses a Stan Ray fleece.
- **Page (version 10).**
  - A pick can carry a fit tip (`sizeNote`), shown on its card, for example "Timberland boots
    run large: try a UK 10.5".
  - Saving a pick now also stores whether it was in his size. The shortlist says "Back in his
    size since it was saved" when that changes.
  - The "Where to look" directory now lists 117 shops.
- **46 new picks with photos and stock in his size**, from Universal Works, Solovair, Slam City
  Skates, Urban Industry, Hikerdelic, Folk, howies, Passenger, Alpkit and Montane (all new shops),
  plus Cernucci, Montirex, Original Penguin, Lyle & Scott and Uskees. Most of them are Street, Rave
  and Outdoor pieces, the styles with the fewest picks.
- **20 new outfits**, including a whole outfit for £57 (Under £60) and a smart one at about £150.
- **The Friday refresh** now adds the shop's photo to new picks (as `img`), sets fit tips, and
  checks the new shops' feeds.
- Totals: **886 picks, 140 outfits, 85 shops; 578 picks with a photo in the packs.**

## 2f. More photos (5 Oct 2026, late)

- ASOS blocks cloud servers, but the public image service wsrv.nl can still fetch its photos.
  The photo address is built from the product number and a colour code
  (`tools/asos_photos.py`).
  - This gave **176 of 195 ASOS picks** a photo.
  - Each one was checked by eye against the pick's name and colour.
- Next's image server answers directly, so both Next picks now have photos. So do Rohan's
  Range jeans and the New Balance 574s from Zalando.
- **758 of 886 picks now show the shop's photo** (page version 11, pack 5).
- Still drawings:
  - 19 ASOS picks whose colour code could not be found
  - 28 Vinted, eBay and Marrkt searches
  - 31 M and M Direct picks and a few M&S, H&M and John Lewis picks that link to a brand or
    category page rather than one product
  - About 35 picks from shops that hide their photos from every tool tried: Zara, COS,
    Arket, Decathlon, The North Face, WoolOvers, Schuh, Joules, Hawes & Curtis, Suit Direct
    and others
- Giving the M and M Direct picks single-product links would let them have photos too.

## 2g. Cheaper first and a sale section for each style (5 Oct 2026, evening)

- **Cheaper first.** In Picks, the recommended order is now half the curated rank and half
  price within each type, so cheaper picks rise without burying the best ones. Outfits do the
  same within each occasion. The builder's suggestions lean slightly towards pieces under £50.
- **A sale section for each style** ("Classic on sale", "Rave on sale" and so on), placed under
  the style intro:
  - It has its own advice and a list of the shops with the best sales for that style.
  - Counts show how many items are reduced, under £20, half price or more, and confirmed in his
    size.
  - Filters for type (the style's key types come first) and price (under £20, £40 or £75), and
    an "only in his size" switch.
  - It is sorted by best value, which weighs the reduction against the price, so a £12 tee at
    40% off sits above a £180 coat at 45% off. It can also sort by cheapest or biggest % off.
  - It shows 12 at a time, with a "Show more" button.
- **The Friday refresh** now aims for at least half of each week's new items under £40, at least
  three new reduced items under £25 per style, and an outfit under £60 where possible.
- Page version 12.

## 2h. Views, finer categories, two new styles and high-street shops (5 Oct 2026, night)

- **One view at a time.** The bar now switches between Shop, Sale, Outfits, Build, Shortlist and
  Style guide, instead of one long scrolling page. The choice is kept in the address (#shop,
  #sale and so on) and remembered on each device.
- **Finer categories, like ASOS.** Shop opens on departments (Clothing, Shoes, Accessories,
  Loungewear and nightwear, Sport and swim, Socks and underwear). Each department shows a tile
  for every category, with a photo, a count and the lowest price. Each list holds one kind of
  thing: jumpers apart from sweatshirts and fleeces, jeans apart from chinos and cargos, trainers
  apart from boots, and so on, 40 categories in all.
  - The category is worked out from each pick's type and name (`subOf` in the page), so no data
    change was needed. The Friday refresh now names new picks with the garment type in plain words.
  - Search results are split by category too. Filters fold away under "Filter".
  - The sale sections use the same categories.
- **Two new styles:** Mod and skate, and Holiday and summer. Each has its own guide, sale section
  and eight outfits. 169 older picks were added to them through `meta/styletags`
  (`data/styletags.json`), and new picks carry the style themselves.
- **78 new picks**, most under £40:
  - 42 for the new styles from Original Penguin, Lyle & Scott, Fred Perry (Jean Store), Farah,
    Community Clothing, Base London, Brakeburn, Savile Row Company, T.M. Lewin, Slam City
    Skates (Last Resort, Polar, Passport), Fila, Albam, howies, Passenger and Uskees.
  - 36 from high-street and value shops: Matalan (14, with its 20% online
    sale), Peacocks (10) and Blue Inc (5), all new to the guide, and 7 more from Mountain Warehouse.
- **"Where to look"** now lists 134 shops, including Jack & Jones, Burton, boohooMAN, New Look,
  Pull&Bear, Bershka, Mango, Ben Sherman, Jacamo, Shoe Zone, Millets, Blacks, Weird Fish and USC.
  Several of these block cloud servers (Primark, TK Maxx, F&F, Very, New Look, Jacamo, Mango),
  so they are links only.
- `tools/ld_reader.py` reads price, photo and stock per size from any product page that
  publishes schema.org data (Matalan, Peacocks and many others).
- Page version 13. Totals: **964 picks, 156 outfits, 88 shops with picks.**

## 2i. Workwear for the job, and another round of picks (5 Oct 2026, late night)

- **New style: Workwear** (`job` in the data), for manual work. Emma's rules, which the Friday
  refresh now follows word for word:
  - Work trousers and shorts are **100% cotton only** (Dave has sensitive skin). Each one was
    checked on the product page. Polycotton, stretch and recycled-polyester blends are out, and
    so is Cordura reinforcement (Blaklader 1556, 1534 and X1500; Uskees ripstop is 60% cotton).
  - Work trousers and shorts are **black, or very dark grey at most**. Brown, stone, navy and
    olive pieces that were tagged Workwear went back to their other styles only.
  - **Safety boots are extra wide only: EE, 4E or 6E**, with a toe cap. The plain "wide fit"
    Apache, Solid Gear, DeWalt and Buckler boots were removed. What is left: Grafters 4E (from
    £32.99), Amblers AS803 EE (£49.88), Rock Fall Otus 6E (£99.99) and Wide Load 6E (£174.99).
  - No T-shirts, since work provides them. Jackets, gilets and jumpers in any dark colour.
  - The page has a "Safety boots and shoes" category and a Workwear guide, sale section and ten
    outfits. 32 picks in all.
  - Gap: no black 100% cotton *cargo* shorts could be found in Dave's size. The shorts on offer
    are Stan Ray black denim, Colorful Standard black twill and Passenger charcoal.
- **87 new picks** since version 13, 64 under £40 and 65 reduced, from Brakeburn, Blue Inc,
  Community Clothing, Fila, Folk, howies, Lyle & Scott, Montirex, Original Penguin, Peregrine,
  Passenger, Stan Ray, Savile Row Company, T.M. Lewin, Uskees, Workwear Gurus, Wide Shoes,
  Cernucci and Colorful Standard. **25 new outfits.**
- **Where to look** gained a "Cheap online, delivered" group: Shein, Temu, Amazon Fashion,
  Debenhams, eBay and Vinted, with a note that sizes run small. Shein puts up a CAPTCHA and
  Temu only renders in a browser, so neither is read automatically; they are links only.
  Wide Shoes (4E and 6E boots) joined the workwear group.
- Page version 15. Totals: **1051 picks, 181 outfits, 94 shops with picks.** The two load
  queries hold about 683 and 368 picks (limit 1000 each, aim under 900).

## 2j. Eight tabs, 101 more picks and 30 more outfits (5 Oct 2026, late night)

- **Fewer, clearer style tabs.** Classic and Casual shared about half their picks, Minimal sat
  mostly inside Classic, and Street mostly inside Casual. The bar now has eight tabs:
  Classic, Casual and street, Mod and skate, Rave, Outdoors, Holiday, Workwear and Lounge.
  - Minimal is a "Within" chip under Classic, next to "Tailored and smart" and "Heritage"
    (renamed from "Heritage and workwear" so it isn't confused with the Workwear tab).
  - Street is a "Within" chip under Casual and street, next to "Out with friends".
  - Each chip keeps its own style guide and sale notes, and old links such as #street or
    #minimal open the right tab and chip.
  - Nothing was lost: the data keeps the minimal and street tags, and the page folds them in
    when it loads (`MERGED` and `SUBBY` in the page). Classic now shows 717 picks and Casual
    and street 725, with every outfit still in place.
- **101 new picks**, 92 under £40 and 99 reduced, mostly 50 to 80% off. Ten new shops:
  - Lambretta, Pretty Green, Gabicci and Merc (mod)
  - Duck and Cover and Tokyo Laundry (cheap basics, lounge sets, boxers)
  - Tog24 (fleeces, gilets, shirts, swim shorts from £6)
  - Speedo and Ellesse (swim and terrace polos)
  - Millets now has picks as well.
  - More shoes from Herring, Base London and Slam City, and a Wide Load 6E composite toe
    safety boot for Workwear.
  - Every photo was checked on a contact sheet. Two that showed the wrong thing were dropped.
- **30 new outfits**, at least two for every tab:
  - 8 Holiday, 6 Mod and skate, 4 Workwear (from £86), 2 Rave, 3 Casual and street,
    3 Classic and minimal, 2 Outdoors and 2 Lounge.
  - Every tab now has at least 14 outfits.
- Page version 16. Totals: **1152 picks, 211 outfits, 105 shops with picks.** The two load
  queries hold about 743 and 409 picks (limit 1000 each).

## 2k. Workwear rebuild, a more lifelike Dave, and dropdowns instead of chips (5 Oct 2026, late)

- **Workwear, rebuilt around Emma's answers:**
  - **6E boots:** every 6E safety boot that could be found is listed. Only the Wide Load range
    (Wide Shoes) and Rock Fall Otus make 6E with a toe cap in the UK. Four are in stock in
    UK 11; five more Wide Load models (690BLWC, 290BSC, 690SZC, 490BPO, 690WZ) are sold out in
    11 and are listed as "sold out" so the page flags them when they come back.
  - **4E boots:** Cofra RAP and FUNK (Wide Fit Shoes) were added alongside the Grafters range.
  - **Shorts:** cargo and plain, black or very dark grey. 100% cotton: Portwest WX1 cargo
    work shorts (£11.51), Luke 1977 Molfre carpenter shorts (£19), Stan Ray A shorts,
    ICHPIG workshop shorts and Polar Jiro. Near-100% (98% cotton, 2% elastane) and marked as
    such: Lambretta cargo shorts, T.M. Lewin chino shorts and Duck and Cover chino shorts.
  - **Trousers:** 100% cotton Portwest WX1 (from £13) and Fristads Kansas, plus near-100%
    Carhartt Rigby, Carhartt double-front and Portwest KX3, all marked with their blend.
  - **Belts for bottoms with few pockets:** Snickers and ToughBuilt clip-on holster pockets
    and pouches, Carhartt 7-pocket and half-apron tool belts, Fristads and Helly Hansen tool
    belts, and a Carhartt cotton duck belt.
  - **Trade brands:** Carhartt (black Detroit, Super Dux, Gilliam, Galesburg), Snickers,
    Helly Hansen, Dickies, Scruffs, Portwest, DeWalt, TuffStuff and Regatta Professional,
    from Workwear Gurus, Trade Workwear (new), Wide Fit Shoes (new) and TuffStuff (new).
  - Fashion pieces (khaki Peacocks jacket, Matalan khaki jumper, Brakeburn shacket) moved
    out of Workwear. Two Tokyo Laundry shorts and a Carhartt "shadow" short stayed out
    because they are mid grey.
  - New `fabric` field on items, shown on each card. A Workwear dropdown under Filter
    shows 6E boots only, 4E and 6E boots, cargo or plain shorts, belts and holsters, or
    100% cotton only.
- **Style options tidied:**
  - The "Within" chips and "Quick sets" chips are gone (Emma prefers dropdowns). Look
    (Clean minimal, Relaxed street, Heritage and so on) is a dropdown in the Shop, Sale and
    Outfits filters, and Collection (Winter, Christmas, Holiday, Gifts) is a dropdown in the
    Shop filter.
  - Lists show at most two colours of the same product, so one polo in six colours no
    longer fills a page.
  - Items now count towards at most three tabs.
  - Picks load in five groups (knit, polo, trouser, shirt and coat, everything else), so the
    old 1000-item ceiling no longer limits the collection.
- **A more lifelike Dave in the outfit drawings:**
  - A slimmer, taller build, a mop of dark curls, a ginger-brown moustache, light stubble
    and fairer skin, all taken from photos Emma shared. The photos themselves are not
    stored anywhere.
  - Light and shade on every garment, elbow and knee creases, a trouser break, thumbs,
    laces, and toe caps on safety boots. Tool belts and holster pockets are drawn on the
    hips.
  - When most pieces in an outfit have a shop photo, the right-hand side of the outfit card
    shows the real photos, head to toe, instead of drawn icons.
- **Another round of picks and outfits:**
  - 39 general picks from three new shops: Weekend Offender, Luke 1977 and Closure London
    (mostly 60 to 80% off), plus Cyberjammies and more shoes, swim and accessories.
  - 49 Workwear pieces.
  - 28 new outfits, 10 of them Workwear (belts, holsters, cargo and plain shorts, and
    4E and 6E boots).
- Page version 17. Totals: **1240 picks, 239 outfits, 111 shops with picks.**

## 2l. Cheaper extra wide work boots, and picks across every style (5 Oct 2026, night)

- **Affordable extra wide safety footwear (13 new pairs, UK 11 in stock):**
  - Grafters 4E (EEEE) at four shops that undercut Wide Shoes:
    - Hollands Country Clothing: 4-eyelet shoes £21.95, dealer boots £22.90,
      7-eyelet boots £24.95, water-resistant brown dealers £33.95. EU sizes; EU 46 is UK 11.
    - Universal Textiles: lace-up shoes £27, dealer boots £30, pull-on dealers £46.
    - Hirst Footwear: brown M9509B dealer boots £35.95.
  - The UKD Grafter 4E range at Work+Safety, all £74.95: Bedrock and Latitude (S1P),
    Expanse (S3 dealer boots) and Grit (S7 waterproof).
  - Mongrel 461 EEE side-zip boots at Big Boots (£124.99).
  - No new 6E safety footwear turned up. The Wide Load range and Rock Fall Otus are
    still the only 6E pairs with a toe cap in the UK.
- **30 general picks:**
  - Brakeburn, Closure London, Duck and Cover, Luke 1977, Lambretta, Pretty Green,
    Weekend Offender, Tog24, T.M. Lewin and Tokyo Laundry.
  - Most are reduced and under £20: puffer, hybrid jacket, knits, tees, long-sleeve polo,
    shirts, cord cargo shorts, board and swim shorts, sandals, a cap, a scarf, a tie and a
    tie slide.
- **29 new outfits:**
  - 12 Workwear outfits built on the new 4E boots. They use cotton shorts or trousers and
    a belt, holster, pouch or apron. Two cost under £60 all in (£45 and £55).
  - 17 across Classic, Minimal, Casual, Street, Mod, Rave, Holiday, Outdoor and Lounge.
- The directory lists the five new boot shops, and the Workwear guide names them.
- The Friday routine now checks these shops for wide boots. It also looks each week for
  more extra wide safety footwear under £50.
- Page version 18. Totals: **1283 picks, 268 outfits, 116 shops with picks.**

## 2m. 17 more shops, and more in every area (5 Oct 2026, night)

- **New shops (17):**
  - Mod and skate: Jump the Gun (a Brighton mod shop), Admiral (up to 75% off) and Flatspot.
  - Street and rave: SikSilk, Criminal Damage and Oi Polloi.
  - Classic: Percival (up to 70% off) and Kestin.
  - Holiday and surf: Saltrock and Animal (up to 76% off).
  - Outdoor: Sealskinz (waterproof gloves, socks and hats) and Urban Excess (Columbia, Bhode).
  - Lounge, socks and gifts: Bamboo Clothing, TBCo and Thought.
  - Rokit for vintage, and Wynsors for cheap shoes and slippers.
- **71 new picks**, most of them reduced:
  - **Workwear (11):**
    - Apache Barkerville cargo trousers (£20.74) and Portwest KX3 winter cargos. Both are
      98% cotton with 2% elastane, and say so on the card.
    - Clip-on holster and nail pockets (Mascot and Fristads), Snickers hammer and long tool
      pouches, and a Fristads leather tool belt.
    - Cofra Off Shore EE side-zip safety boots, and brown UKD Grafter Expanse and Grit
      4E boots.
    - Sealskinz waterproof fleece-lined gloves.
  - **Other styles:** knits, hoodies, tees, a padded jacket, a longline waterproof,
    windcheaters, track jackets, oxford and Cuban shirts, board and swim shorts,
    flip-flops, walking shoes, slippers, bamboo loungewear, sock gifts, a tie bar and a
    vintage silk tie.
- **28 new outfits:**
  - 6 Workwear: holsters, a hammer pouch, a nail pocket, a leather tool belt and a long
    pouch, worn with cotton cargos or shorts and 4E or EE boots.
  - 22 across Casual, Street, Mod, Rave, Holiday, Classic, Outdoor and Lounge.
- I checked Timberland PRO, Tradesman Workwear, Safetywear, Wynsors and Amblers.
  None had new EE or wider safety footwear in UK 11.
- The directory lists all 17 new shops, and the Friday routine checks them.
- Page version 19. Totals: **1354 picks, 296 outfits, 133 shops with picks.**

## 2n. Every shop searched for every kind of item (5 Oct 2026, night)

Emma noticed that a shop was often used for one kind of thing only (one shop for shoes,
another for jumpers) and never checked for anything else. So every shop was swept across
its whole range.

- **How it was done:**
  - Read the full catalogue of about 85 shops (everything that publishes one in pounds),
    plus six more that had never been pulled: Samuel Windsor, Mrs Bow Tie, Philip Morris
    Direct, Stuarts London, Marrkt and Twisted Tailor.
  - Sorted every product into 25 kinds: jumpers, hoodies, fleeces, polos, tees, shirts,
    overshirts, jackets, gilets, jeans, trousers, joggers, shorts, swim, loungewear,
    slippers, trainers, shoes, boots, sandals, hats, bags, belts, small accessories and
    socks.
  - For each shop, listed the kinds it sells in Dave's size that had no picks yet (about
    900 gaps). Then added the best reduced pick for up to six kinds per shop.
  - Matalan and Peacocks aren't on Shopify, so they were read from their own product
    data. Matalan gained hoodies, joggers, shorts, a knitted polo, brogues, trainers,
    Chelsea and chukka boots, slippers, pyjamas, swim shorts, sliders and a flat cap.
    Peacocks gained a hoodie, shirt, joggers, dressing gown, flat cap, gloves and braces.
  - Every photo was checked on contact sheets. Women's, kids', mismatched or
    wrong-colour items were dropped, along with sizes that wouldn't fit (suit trousers in
    40 inch, S/M-only hats).
- **357 new picks** from 78 shops. Most are reduced: 244 have a "was" price and 188
  are under £40.
- **26 new outfits**, many of them head to toe from one shop: three from Matalan, plus
  Peacocks, Lambretta, Luke 1977, Closure London, Farah, Weekend Offender, Pretty Green,
  Tokyo Laundry, Ellesse, Berghaus, Montane and Passenger. There are also two dressing
  gown nights in, holiday looks and more.
- Workwear shops were not part of the automatic sweep, because the Workwear rules
  (100% cotton, black, extra wide safety boots) need checking by hand.
- The Friday routine now runs this sweep every week before adding new shops, and has
  instructions for reading Matalan and Peacocks.
- Page version 20. Totals: **1711 picks, 322 outfits, 141 shops with picks.**

## 3. Next steps

### Step 1: Photos still missing
Most shops are done (see 2f). The gaps are shops that block cloud servers: 19 ASOS picks, Arket, COS,
Zara, Next, Joules, The North Face, Converse, Decathlon, Zalando, H&M, Hawes & Curtis, John
Lewis, Office and Gymshark. Running `python3 tools/fetch_photos.py --only <ids> --out photos`
from a home computer usually gets past them. Then add the new pack to the page and to
`meta/photos`.

### Step 2: Data hygiene (each weekly refresh)
- Re-check every pick whose `checked` date is over 30 days old: prices, links and his size.
  Remove dead links rather than leaving "No longer listed" gaps in outfits.
- Set `added` only on picks that are actually new (see gap 4), so "New this week" means
  something again.
- Store `img` (or refresh the packs) at the same time as the price check, so photos stay current
  with the listing.
- ~~Add a "price seen over a month ago" note to old cards.~~ Done in round two.

### Step 3: Fit and sizes
- Measure Dave: neck plus half an inch, chest under the arms, inside leg. Then update
  `meta/profile` and drop the "to confirm" notes.
- ~~Add a per-shop size note (`sizeNote`).~~ Done in round four. More can be added as fit tips
  turn up.

### Step 4: Page features worth adding
1. ~~**Photo-first view.**~~ Done in round two as the compact grid.
2. **Photo strip on outfit cards:** under the drawing, a row of the pieces' listing photos, once
   coverage is good.
3. ~~**Price-drop watch on the shortlist.**~~ Done in round two.
4. **"Shop by budget" quick sets:** an outfit for £60, £100 or £150, drawn from the builder's
   suggestion engine and refreshed weekly.
5. ~~**Shop filter in Picks.**~~ Done in round two.

### Step 5: More stores to add next
These are in the directory but still have no picks: Gap, Levi's, Dr Martens direct, Vans,
New Balance direct, Timberland direct, Berghaus direct, Urban Outfitters, Pull&Bear, Bershka,
TK Maxx, BrandAlley, Very and F&F. The search index had only old or US prices for Gap and Levi's
this round. Check them again when they can be reached directly. Next round: aim for 3 to 5 picks each, and favour sale stock and
pieces that slot into existing outfits.

---

## 4. Review of the live page (version 21), and the plan for version 22

Reviewed on 5 Oct 2026 against the live artifact, its database and the Friday refresh routine,
not the copy in this folder. Checked twice: the second pass corrected several figures (see 4.8).
**This folder is one version behind:** the live page has an "All styles" tab, five more Workwear
shops (Rock Solid Safety, Tiger Safety, Best Workwear, DeWalt Workwear, Timberland PRO) and the
97% cotton rule, and the database holds **1,861 picks and 334 outfits** against 1,711 and 322
here.

### 4.1 What the numbers show

| Area | Now | Problem |
|---|---|---|
| Page weight | 948 picks carry their photo inside the database row: 8.5 MB of the 9.4 MB of pick data. The other 755 photos sit in 5.6 MB of photo packs. | About 15 MB arrives on every visit. Without the photos the picks are 0.8 MB. `loading="lazy"` does nothing, because the picture is already inside the data. This is the main reason the page is slow on a phone, and it grows by about 1 MB every Friday, because the refresh adds up to 45 photos a batch inside the rows. |
| Photo size | The refresh aims for under 25 KB a photo, but rows hold photos of up to 60 KB | Some batches went over the target. |
| Status line | `meta/status` says 1,781 picks; `meta/photos` says 758 photos | Both are out of date (1,861 picks; 1,703 with a photo). The refresh rewrites `meta/status` each Friday, but the extra rounds since then didn't. |
| His size | 1,247 confirmed, 52 not in his size, **562 unknown (30%)** | ASOS 195, M and M Direct 31, M&S 30, Vinted 28, Charles Tyrwhitt 18, WoolOvers 13, Moss 13. The card already says "His size: L. The shop does not show stock", so this is about checking more, not labelling. Shirt and jacket sizes are still "to confirm". |
| Colour | 521 pick names say black, against 208 navy, 45 stone, 19 olive and 7 burgundy | No cap on any colour (Emma, 5 Oct). A colour filter makes the other colours easier to find. |
| Pick use | **1,028 of 1,861 picks are in no outfit** | Half the catalogue is never shown worn. |
| Outfit occasions | 217 everyday, 49 party, 30 smart, 28 lounge, **10 event** | Hardly anything for weddings, christenings, funerals, interviews or a work Christmas do. Casual has 7 smart or party outfits and Street 8. |
| Outfit weather | **41 wet** of 334; Holiday has 0 cold or mild; Lounge has 5 warm | There are 74 coats tagged for wet weather, so the gap is outfits, not stock. |
| Outfit cost | Median £122; 25 under £60; 68 over £200 | Not enough cheap outfits for a page whose rule is "cheaper first". |
| Thin categories | Tailoring 18, Sport 27, Basics 30, Swim 33 | Tailoring already has navy and charcoal suits (Moss, Suit Direct) and blazers. What's missing is shirts with a collar size, ties, dress shoes and smart accessories. |
| Pieces | 83 outfits have only 3 pieces | Many are missing a layer, belt or bag that would finish them. |
| Links | 38 picks link to a brand or category page instead of one product: 31 M and M Direct, 6 M&S, 1 Office | These can't show a single price, photo or stock. (The 28 Vinted, 2 eBay and 1 Marrkt searches are meant to be searches.) |
| Same product twice | 5 products are listed at two shops each (Grafters M9509B, M9504A and dealer boots, TuffStuff Stanton softshell, Rock Fall Otus); one Vinted Barbour search is in twice | The two-shop pairs are useful for comparing prices, but they show as two cards. Show one card with the cheaper shop and a "also at" line. Remove the repeated Vinted search. |
| Workwear | 50 of the 51 Workwear trousers and shorts have a `fabric` line | `rv-cernucci-cargo` says "100% cotton" in its note but has no `fabric` field, so the "100% cotton only" filter hides it. |
| Load groups | The refresh's note for 5 Oct says "everything else" holds 649 picks, with a ceiling of 900 | Adding the 300 picks below (many of them accessories, shoes, tailoring and basics) would push that group over. |

### 4.2 What already works well (keep it)

- The structure: one view at a time (Shop, Sale, Outfits, Build, Shortlist, Style guide), 40
  categories, eight style tabs plus All styles.
- Every outfit is drawn on Dave and every piece is priced and linked. No outfit links to a
  missing pick or to a pick out of his size.
- The Workwear rules are kept carefully: cotton at 97% or more with the blend shown, black or
  charcoal, no slim fits, and EE to 6E toe-cap boots. Every Workwear boot is marked extra wide.
- Price-drop and back-in-size notes on the shortlist, old-price warnings, fit tips, and a size
  line on every card.
- The Friday refresh already re-checks every price and size, writes `prev` when a price changes,
  adds at least 40 picks and 2 to 4 outfits, and follows the votes.
- "New this week" will sort itself out: it counts picks added in the 7 days before the latest
  check, so the 1,288 picks dated 5 October drop out after the refresh on 16 October.

### 4.3 The upgrade, area by area (version 22)

#### A. Speed and data (do first, everything else depends on it)
1. **Take photos out of the pick rows, without the asset store.** The refresh can only write
   database rows (it may not republish the page), and the asset store would end public link
   sharing (a page that uses it can only be opened inside the organisation). So:
   - Move each `img` into its own row in a new `photos` collection, keyed by pick id. Pick rows
     drop to about 0.8 MB in total.
   - The page fetches a photo row only when its card scrolls into view, and keeps it in the
     browser cache.
   - The refresh writes new photos to `photos/<id>` instead of `img`, at 25 KB or less.
   - The five existing photo packs stay as they are.
   - Target: under 2 MB before the first screen shows, and growth on Fridays no longer slows
     the page.
2. **Count on the page.** The page counts picks, outfits, shops and photos itself, so a stale
   `meta/status` or `meta/photos` can't mislead.
3. **Fix the data:** single-product links for the 31 M and M Direct, 6 M&S and 1 Office picks
   (or remove them); one card for the same product at two shops; remove the repeated Vinted
   search; add `fabric` to the Cernucci cargo.
4. **Add a sixth load group** (for example shoes on their own) before the new picks go in.
5. **Bring this folder up to date:** copy the live page into `page.html` and the live data into
   `data/` (without photos).

#### B. Shop
1. **Colour filter:** navy, black, grey, stone, olive, brown, green, burgundy, ecru, blue. Use the
   same colour words as the outfits.
2. **"Goes with" on each card:** three picks from other categories that suit it, plus the
   outfits that already use it.
3. **"Cheaper like this":** the cheapest picks in the same category and colour, shown on the card.

#### C. Sale
1. **Price history line** on each card ("was £60, £45 on 29 Sep, now £30"). The refresh only
   keeps last week's price in `prev`, so it would also need to keep a short list of earlier
   prices.
2. **Delivery threshold note** per shop ("free delivery over £50"), so cheap single items aren't
   cancelled out by postage.

#### D. Outfits
1. **"What to wear today":** choose occasion and weather (cold, mild, warm, wet) and get three
   outfits, putting first those that use pieces already bought from the shortlist.
2. **Swap a piece:** each piece gets a "swap" button that offers cheaper or different-colour
   picks of the same kind and updates the total.
3. **Photo strip** under the drawing (open since the first review).
4. **"£X to finish":** when pieces are marked bought, each outfit shows what is left to buy, and
   it can be sorted by that.
5. **Occasion filter for real events:** wedding guest, christening, funeral, interview, date
   night, gig, football, Christmas party, Sunday lunch, city break.

#### E. Builder
1. **Lock a piece and re-suggest the rest:** keep the boots, rebuild everything else to budget.
2. **Budget split hint:** spend on shoes and coat, save on knit and tees (from the style guides).

#### F. Shortlist
1. **Totals per shop** with the delivery threshold, and a single "buy list" total.
2. **Download the buy list** as a text or CSV file, with links, sizes and prices, to work through
   on a laptop.

#### G. His wardrobe (a separate section at the back)
- **"He has this" on every card:** two choices, "He has this" or "He has something like it". This
  only records it. The Shop, Sale, Outfits and Build views, and the Friday refresh's outfits,
  carry on exactly as now and never use owned pieces.
- **A "His wardrobe" view, last in the bar:** everything marked, plus his own things typed in by
  hand (black suit, New Balance and Nike trainers, crossbody, bum and side bags to start). Here,
  and only here, the page puts together outfits from what he owns, drawn on Dave like the others,
  by occasion and weather.
- Storage: in the artifact, a new `owned` collection (it needs a new database rule, so the page
  is republished once). In Dave's GitHub copy, his marks stay in his browser (section J).

#### H. Style guide and sizes
- A **measuring card** (neck, chest, inside leg) that saves to `meta/profile`. Once filled in,
  drop the "to confirm" notes.
- A **"Dave's colours"** panel: the colours that suit his fair skin, dark hair and ginger-brown
  moustache (navy, olive, rust, camel, burgundy and ecru; mustard and washed-out pastels are
  harder), linked to the colour filter.
- **Care notes** on cards for wool, linen and waxed cotton.

#### I. Drawings
- Shapes the outfits now use but the figure draws plainly: suits with a waistcoat, an overcoat
  over a blazer, knee pads, a neck warmer and a tool backpack (Workwear extras), and swim shorts
  with an open shirt for Holiday.

#### J. Dave's copy on GitHub Pages
Dave will use a copy served from this repo, not the artifact. The repo is public, so GitHub
Pages is free. It is not switched on yet: Settings, Pages, deploy from `main`, root folder.
- **Same page, no database.** When the artifact's database isn't there, the page loads
  `data/items.json`, `data/outfits.json`, `data/meta.json` and the photo files from the repo
  instead. Add an `index.html` so the site address opens the page.
- **His thumbs, shortlist, "He has this" marks and his own outfits stay on his phone** (browser
  storage). They shape what he sees and are not sent anywhere. The page already has a
  device-only mode for the shortlist, so this extends it.
- **Photos as files.** The export writes photos into pack files grouped by category, loaded
  only when that category is opened.
- **Updated only when Emma asks.** A Claude session reads the artifact's database, writes the
  JSON and photo files, and opens a pull request. Merging it updates Dave's site. The page shows
  the export date ("Prices checked 9 Oct") so he knows how fresh it is, and the card's
  "Check before buying" warning appears after 30 days as now.
- Never part of the export: the artifact's shared shortlist, votes, saved outfits and `owned`
  marks (they belong to the people using the artifact).
- **Public by default.** A Pages site from a public repo can be found by anyone. The export would
  publish Dave's first name, sizes and profile notes. Leave the name out of the public copy, or
  make the repo private (Pages on a private repo needs a paid GitHub plan).

### 4.4 More picks (target: about 260 new on top of the Friday refresh's 40 a week)

Fill the gaps the numbers show, mostly reduced and mostly under £40:

| Gap | Now | Add | What |
|---|---|---|---|
| Smart shirts and accessories | Tailoring 18 | 30 | White and pale blue shirts in a 15.5 to 16in collar, ties, pocket squares, tie bars, dress belts and socks, black Oxford and Derby shoes, a smart overcoat |
| Colours with few picks | 7 burgundy, 19 olive, 45 stone | 40 | Olive, stone, brown, burgundy and ecru knits, chinos, overshirts and jackets, for choice (no cap on black or any other colour) |
| Basics | 30 | 25 | Thermals, merino socks, multipacks of plain tees, vests and boxers |
| Sport | 27 | 20 | Gym shorts, training tops and running shoes in UK 11 |
| Rain extras | 74 wet-weather coats already | 10 | Waterproof trainers and boots, a compact umbrella, a smart mac |
| Winter sun and city break (Holiday) | 0 cold or mild outfits | 20 | Light knits, overshirts, a packable jacket, smart trainers and a weekend bag |
| Summer lounge | 5 warm Lounge outfits | 10 | Cotton shorts pyjamas, light robes, sliders |
| Workwear extras | 197 | 25 | Knee pads, base layers, thick socks, a tool backpack and winter gloves, plus black cotton cargo shorts in 34W (still the hardest gap). All checked by hand against the Workwear rules. |
| Directory shops with no picks | 14 shops | 40 | Gap, Levi's, Dr Martens, Vans, New Balance, Timberland, Berghaus, Urban Outfitters, Pull&Bear, Bershka, TK Maxx, BrandAlley, Very and F&F, 3 each. Note: the refresh is told not to fetch Gap, New Balance, TK Maxx, F&F or Very (they block cloud servers), so those need a home computer or stay links only. |
| Size checks | 562 unknown | — | Re-check the size on the ASOS, M&S, Charles Tyrwhitt, WoolOvers and Moss picks where the product page shows it |

### 4.5 More outfits (target: about 120 new, to about 455)

| Gap | Now | Add |
|---|---|---|
| Events (wedding guest, christening, funeral, interview, Christmas party, birthday meal) | 10 | 25 |
| Smart | 30 | 15 |
| Wet weather, across every tab | 41 | 25 |
| Under £60 all in | 25 | 20, at least two per tab |
| Holiday in cold or mild weather (winter sun, city break) | 0 | 8 |
| Lounge for warm nights | 5 | 5 |
| Casual and street, smart or party | 7 and 8 | 8 |
| Capsule: one 12-piece set that makes 20 outfits, shown together | 0 | 1 set, 14 outfits |

Build them from the 1,028 picks in no outfit first, and give every 3-piece outfit a fourth piece
where a layer, belt or bag would finish it. These outfits never use owned pieces; the outfits
in "His wardrobe" are put together by the page from what is marked there.

### 4.6 Changes to the Friday refresh
- Write photos to `photos/<id>` rows instead of `img`, at 25 KB or less (A1).
- Keep a short price history per pick, not only `prev` (C1).
- Respect the sixth load group (A4) and update the group sizes in its notes.
- Report the occasion and weather gaps each week, and close the biggest gap first when choosing
  new outfits.
- Keep the owned-clothes rule as it is, and never read or write the `owned` collection.
- The routine has 12 connectors attached (Gmail, Google Drive, Spotify, Lucid and others) that a
  clothes refresh never uses. Removing them would be safer, especially Gmail.

### 4.7 Order of work
1. Section A (speed and data), and the refresh changes in 4.6. One round.
2. Section J (Dave's GitHub Pages copy), with the first export, so he has it early.
3. Sections D and E (swap, lock, what to wear today, "£X to finish").
4. Sections B, C and F (colour filter, price history, buy list download).
5. Sections G, H and I (his wardrobe, measuring card, drawings).
6. Picks (4.4) and outfits (4.5), spread across every round. Export to Dave's copy when asked.

### 4.8 Corrections made on the second review
- Photos: the first draft suggested the asset store. It would end public link sharing, and the
  refresh can't use it, so A1 now uses a `photos` collection.
- "New this week" is not broken: it sorts itself out after 16 October.
- "Size unknown" labels already exist on the cards. The task is to check more sizes.
- The 8 "unpriced" pre-owned picks were 31 searches that show a price range, as designed. Not a
  fault.
- The Cernucci cargo is 100% cotton (it says so in its note). It only lacks the `fabric` field.
- Brand-page links: 38, not 14.
- The duplicates are mostly the same product at two shops, which is useful.
- Tailoring already has navy and charcoal suits, so the gap is shirts, ties and shoes.
- There are 74 wet-weather coats, so rainwear needs outfits more than picks.
- Owned clothes: the Friday refresh forbids outfits built round them, so G is a separate section
  that never touches the main views.
- The refresh already re-checks prices weekly, so the plan no longer says "once a fortnight".

### 4.9 Emma's answers (5 Oct 2026)
1. **His own clothes:** don't use them in the existing sections. Add a "he has this, or something
   like it" mark, and a separate "His wardrobe" section at the back that styles outfits from them
   (G).
2. **How Dave uses it:** through the GitHub version (J), with his thumbs and shortlist on his
   device only. It is updated only when Emma asks, and served as a GitHub Pages site.
3. **Ask the stylist:** left out.
4. **Colours:** no cap on any colour. The "not black" switch and the builder's colour warning
   are removed. The colour filter stays.

Still open:
- **His measurements** (neck, chest under the arms, inside leg), so the "to confirm" sizes can
  go.
- **Switching on GitHub Pages** in the repo settings (Emma's step, once the page is ready).
- **Privacy of the Pages copy:** is it fine for his sizes and first name to be on a public site?
