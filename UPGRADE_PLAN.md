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

## 2o. Workwear sweep, an "All styles" tab and more wide-boot shops (5 Oct 2026, night)

- **"All styles" tab:** the first style button now shows every pick and outfit at once.
- **Workwear sweep across every shop:** black or charcoal shorts at 97% cotton or more
  from any shop (cargo first, not only "work" shorts), plus work accessories: knee pads,
  neck warmers, socks, beanies, gloves, base layers, ear defenders, braces, tool belts
  and a tool backpack.
- **New extra wide (4E) safety footwear shops:** Rock Solid Safety (Grafters from
  £22.99) and Tiger Safety (from £24.78).
- 70 new picks and 12 Workwear outfits. Page version 21. Totals: 1781 picks, 334 outfits.

## 2p. No slim fits, more 6E boots and 20 more shops (5 Oct 2026, night)

- **No slim-fit work trousers or shorts.** Every Workwear trouser and short was checked
  against the shop's own description. Eight were slim or tapered and were removed:
  Carhartt slim double-front and Rigby, Portwest KX3 T801, KX312, S231 and S232, Apache
  Barkerville and Caterpillar Dynamic. The 10 outfits that used them now use relaxed
  100% cotton trousers instead. The Friday routine now skips slim, skinny and tapered
  fits.
- **Wider than 4E:** three Steitz Secura 6E safety boots and shoes at Wide Fit Shoes
  (sold out in every size today, kept as watch items), and the 6E Rock Fall Otus at
  Safety Boots UK for £94.49 (shown as "VAT free"). Nothing wider than 6E was found as a
  safety boot in the UK. DB Shoes do a 6V (6E to 8E) fitting, but those aren't safety
  shoes.
- **20 new shops:** Military Kit, Military Mart, Lifting Equipment Store, Safety Boots
  UK, New Era, Gramicci, O'Neill, Volcom, HUF, KAVU, Jack Wolfskin, Lazy Jacks, Dubarry,
  Goodhood, Mountain Equipment, Padders, Voi Jeans, Timex, Gym King and Henri Lloyd.
- **New Workwear:** black 100% cotton cargo shorts from £24 (New Era canvas Bermuda at
  65% off, Mil-Tec Vintage, Surplus Airborne, New Era cargo), loose Brandit cargo
  trousers, Highlander Magnum cargo trousers, Gramicci G-Pants, O'Neill carpenter
  trousers, belt pouches from £8.95, and cheap Portwest, JCB and TuffStuff fleeces,
  hoodies and gilets.
- 88 new picks and 9 outfits (4 Workwear). Page version 22. Totals: **1861 picks, 343
  outfits, 169 shops with picks.**

## 2q. Restart: mixed styles, a large outfit view, and the catalogue as files (6 Oct 2026)

- **New live page:** <https://claude.ai/artifact/FtdHKgXdaBGrVmpbVYTrLn>. The old artifact
  belongs to another account, so its database (including the later list of about 2,400
  picks pulled from 61,000 shop products) could not be read. This round starts again from
  the 1,861 picks and 343 outfits in this repo.
- **Catalogue as files:** picks, outfits, sizes and photos are published with the page
  (`tools/build_site.py` builds `site/`). The database now holds only what people mark:
  shortlist, thumbs, saved outfits, his wardrobe and his measurements. No more 50-batch
  database loads.
- **Mix styles:** a "Mix styles" button lets several style tabs be on at once (for example
  Holiday + Lounge). "All styles" still shows everything. The choice is remembered.
- **Large outfit view:** tap any outfit drawing (or "View large") for the figure at full
  height next to big listing photos of each piece, with prices and links.
- **Layout:** style tabs wrap on wide screens instead of hiding off the edge, a fade shows
  there are more on phones, and the page is wider on big monitors. Outfits switch to real
  photos when half their pieces have one (was 60%).
- **Blocked:** the cloud environment refused every shop site, so no new picks or photos
  were pulled this round. Set Network access to Full in the project's cloud environment,
  or run `tools/shopify_pull.py` and `tools/fetch_photos.py` from a home computer.

## 2r. Lifelike proportions and photos in every outfit (6 Oct 2026)

- **Proportions:** the figure had a long body and short legs (crotch at 36% of his height,
  fingertips above the crotch). `figFix()` in `page.html` now moves every point between chest
  and ankle so he stands about 7.5 heads tall: waistband at 58% of his height from the floor,
  crotch at 45% (a 32in leg), knees at 27%. The arms keep their length, so the wrists sit level
  with the crotch and the fingertips reach mid-thigh. Hems were reset to match: tees and polos
  end at the hip, shirts a little lower, blazers cover the seat, coats stop above the knee.
- **Detail:** shading on the neck, arms and bare legs (light from the left, as on the clothes),
  a calf shape on bare legs, and fingers and a thumb on each hand. Tool-belt pouches and
  crossbody bags move with the hips rather than the arms.
- **Photos in outfits:** the "pieces" side of each outfit board now shows tiles as soon as one
  piece has a listing photo (was half of them): the real photo where there is one, the drawing
  where there is not. The separate thumbnail strip under the board is gone, since it repeated them.
- **Blocked again:** the cloud environment's network policy refused every shop site (403 from the
  proxy for M&S, Next, ASOS, Workwear Gurus, JD Sports, Matalan, END. and the Shopify feeds), so
  no new picks or photos this round. The catalogue stays at 1,861 picks and 343 outfits.

## 2s. 4,282 more picks, photos for 98%, and a to-scale photo flat lay (6 Oct 2026)

- **The older 2,400-pick list:** not recoverable. The older artifact belongs to another account, so
  its database cannot be read, and its published files are only the page and five photo packs. The
  zip that came with the brief is an older copy of the page (about version 22) with the same packs.
  This round rebuilds a larger list from the shops directly.
- **Pull:** 129 shops in "Where to look" (and the shops behind existing picks) publish a Shopify
  feed. `tools/shopify_pull.py` (now with `--out`, `--pages` and `@hosts.txt`) pulled up to 5,000
  products from each: about 208,000 products from 119 shops.
- **Filter:** the new `tools/sweep_filter.py` turned them into 4,282 picks from 112 shops
  (`data/items-new.json`), so the page now has **6,143 picks**. Its rules:
  - men's only; in stock in his size at the pull: L tops, 15.5 to 16in collars, 40R jackets,
    34W with a 32in or regular leg, UK 11 shoes. A bare "11" counts only when the shop does not list
    US sizes. Short, long and 34in legs are left out (1,098 trousers dropped). Where a shop lists the
    waist only, the card says the leg length is not listed.
  - category from the noun, after removing brand names that contain "jeans" or "polo" (Tommy Jeans,
    Calvin Klein Jeans, Polo Ralph Lauren) and words like "short sleeve", so a short-sleeve shirt is a
    shirt and a Tommy Jeans jumper is a jumper.
  - clean names: no "Special Offer", "Clearance" or "Sale" prefixes (also when the shop puts them in
    the brand field), no doubled brand, no repeated colour, no "Men's", no style codes; long names are
    cut at a word.
  - discounted first: each shop gets up to 60 picks and 14 per kind, filled with reduced pieces first;
    full-price pieces fill at most a third. 3,212 of the 4,282 are reduced.
  - workwear: at least 60% cotton (read from the description), no slim, skinny or tapered fits, and
    safety boots only in 4E, 5E or 6E. Ordinary shoes from the wide-fit shops go to Casual rather than
    Workwear. No slim or tapered trousers anywhere.
- **Photos:** `tools/fetch_photos.py` gained `--prefix`, `--skip-existing`, `--size`, `--fit contain`
  and `--quality`, and uses a pick's `img_src` (the shop's own photo URL from the feed) when there is
  one. New photos are 360 by 450 (4:5), the whole garment on its own background, about 6.6 KB each.
  4,281 of the new picks have one (`photos/new-*.json`). For the older picks, 131 more came from their
  pages (`photos/more-*.json`), and 835 whose shops refuse page downloads were matched to the pulled
  feeds by handle (`photos/more2-*.json`). In total, **6,002 of 6,143 picks have a photo** (98%, was 41%).
- **Load groups:** `tools/build_site.py` now writes the picks as 12 load groups of at most 712
  (`data/items/<group>.json`, listed in `data/items.json`), with shirts and coats each in their own.
  Each group's photos are in `data/photos/<group>.json`. The page fetches the groups in parallel.
- **Outfits:** the large outfit view opens on **Real photos, to scale**: the shop photos laid out
  head to toe at 2.4 units per centimetre (coat about 88 cm, trousers 106 cm, boots 30 cm, a cap
  24 cm), tops side by side, accessories in a column, with a 50 cm scale bar. "On the figure" switches
  back to the drawing, and the choice is remembered. Cards, tiles and the outfit boards now show the
  whole photo (contain, not crop).
- **Published:** version 25 of <https://claude.ai/artifact/FtdHKgXdaBGrVmpbVYTrLn> (43 MB of files).

## 2t. A more lifelike figure, drawn in each piece's real colour (6 Oct 2026)

- **Style tabs (version 26):** the Mix styles button is gone; tap several style tabs to combine them,
  tap one again to drop it, and All styles clears the choice.
- **Neck:** about 70% of the head's width (was half), flaring into the shoulders, with the Adam's
  apple and neck tendons drawn in.
- **Shoes:** drawn from the front at about 11 cm wide each (were 17 cm slabs), with the toe box,
  a sole, welt line, a toe highlight, and detail by kind: laces and a toe cap on trainers, laces up
  the shaft on lace-up boots, elastic sides on Chelsea and dealer boots, a saddle on loafers, a toe-cap
  ridge on safety footwear. Bare feet are narrower to match.
- **Arms and trousers:** sleeves and arms swell slightly at the shoulder and forearm instead of being
  straight tubes; trouser hems curve over the shoe.
- **True colours:** each piece is drawn in the colour of its own shop photo instead of the nearest of
  18 palette colours. The page samples the photo on a canvas (chest for tops, the sides for open
  jackets, the legs for trousers, the whole shoe), leaves out the background and skin, takes the darker
  middle of the main colour, and pulls studio-lit black back to near black. A colour picked by hand in
  the builder still wins.

## 2u. A visual builder, 572 outfits and 200 shops (version 28, 6 Oct 2026)

- **Build:** the dropdowns are gone. A chip for each part of the outfit (with its photo once
  chosen), then that part's pieces as photo tiles with price, saving and shop. Tap a tile, or drag
  it onto the figure, to put it on; tap again or "Take it off" to remove it. Filter and sort the
  tiles; Keep and Suggest still work. On phones the figure sits on top.
- **Drawings match the listings:** 23 outfit pieces were drawn as the wrong kind of garment
  (overshirts as jackets, puffer jackets as long coats, a parka as a jacket) and 51 in the wrong
  colour; all corrected. The page's own shape rules now read hoods, knitted polos, gilets, vests,
  overshirts, slippers and more trainer names correctly.
- **Figure:** Dave's shorter curls (on top, trimmed above the ears), short beard and moustache,
  eyes and brows, from his photo. Parkas, waterproofs and puffers get a hood, zips, flap pockets and a
  waist cord. Graphic tees show a chest print; mod polos tipping; pocket tees, henleys, zip hoodies,
  rugby stripes, button-down collars and gum soles are drawn when the listing names them. Checks
  and stripes take the item's second colour from its photo.
- **Outfits:** `tools/make_outfits.py` adds 229 outfits (`data/outfits-new.json`) across all eight
  styles, from photographed picks in his size: weather-matched, at most one non-neutral colour,
  safety footwear for Workwear, no joggers outside Lounge and Rave, reduced pieces first, no pick in
  more than two. 572 outfits in all.
- **Shops:** 78 more UK shops in "Where to look", including a new Premium brands group (Reiss,
  AllSaints, Ted Baker, Hackett, Paul Smith, BOSS, Tommy Hilfiger, Ralph Lauren, Lacoste, Stone
  Island and more) and Fred Perry, Barbour, House of Fraser, Flannels, Mainline, Scotts, Footasylum,
  size?, Skechers, Clarks, Loake, Grenson, Barker, Hotter, Cosyfeet, Spoke, BadRhino, Craghoppers,
  Rab, Patagonia, Helly Hansen, Engelbert Strauss and Snickers. `tools/sitemap_sweep.py` reads shops
  without a Shopify feed through their sitemaps and schema.org data: 9,303 products from 48 shops,
  filtered to 1,012 picks (`data/items-shops.json`, 948 with photos). The page now has 7,155 picks
  from 200 shops. About 30 shops refuse automated requests (Fred Perry, Ralph Lauren, Lacoste, TK
  Maxx, Mr Porter, Dr Martens and others) and are links only. Picks from shops that do not publish
  stock by size show his usual size instead of "in stock".

## 2v. Original face, curlier hair, a 3D model and 131 more photos (version 29, 6 Oct 2026)

- **Face:** back to the version 27 face (the moustache, dot eyes, thin brows), with the moustache in the
  ginger-brown of his photos.
- **Hair:** from his photos: dark, tightly curled ringlets with height on top, a few loose curls over
  the forehead, and the sides falling to about the bottom of the ears. Each curl is a ringlet with an
  open spiral stroke.
- **3D model:** a third view in the large outfit view. Three.js (r128 from cdnjs) loads only when it is
  opened. Dave is built at 1.83 m with the drawing's proportions, his curls and moustache, and each
  piece as cloth over the body in its photo colour and pattern (check, stripe, denim, knit, cord,
  quilt): tops, knits and jackets layered and open where worn open, trousers or shorts, shoes or
  boots, and hats, sunglasses, watch, bag, scarf and chain. Drag to turn him; he turns slowly until
  touched (not with reduced motion). The view stops when closed.
- **Photos:** the headless-browser fallback (`fetch_photos.py --browser`, now with relative photo URLs
  resolved) found 131 of the 174 picks still without one. 7,081 of 7,155 picks now have a photo.
- **Shops behind bot protection:** `tools/browser_sweep.js` (sitemaps and product pages through headless
  Chromium) is written, but Fred Perry and John Lewis still refused it from this cloud server. The
  shops in the "links only" list stay links for now.

## 2w. A 2D/3D switch, a better 3D model, and a review of the whole page (version 30, 6 Oct 2026)

- **2D or 3D, page-wide:** a "Dave: 2D drawing / 3D model" switch in the top bar. In 3D, outfit cards,
  "What to wear today", "One piece, many outfits" and saved outfits show still 3D renders (one hidden
  renderer, cached by outfit and colours, so the page never opens more than three 3D views); the
  builder and the large outfit view show the live model you can turn. The choice is remembered.
- **Turning 2D off later:** Style guide > Page settings > "Offer the 2D drawings". Off, Dave is shown
  only in 3D everywhere and the 2D buttons disappear. The page owner's choice is saved for everyone
  (database `meta/settings`); anyone else's stays on their device. It is on until changed.
- **Better 3D model:** a chin and jaw, eyes with whites, brows, a nose, a single curved moustache;
  ringlet curls (small tori and beads) over a dark cap that stops at the hairline in front and at
  the bottom of the ears behind; shoulders, hands with thumbs; cloth with a fine weave that catches
  the light; ribbed hems and cuffs on knits, crew necks, roll necks, hoods with drawcords, shirt and
  polo collars with plackets and buttons, blazer lapels, zips on zip jackets and half-zips, chest and
  cargo pockets, waistbands and flies; trainers with white or gum soles and laces, boots with shafts;
  beanie, cap, bucket hat, sunglasses, watch, bag, backpack, scarf, chain and tie.
- **Review of the rest of the page** (desktop and phone, every view): no errors, no sideways scroll,
  data loads in about a second. Fixed now:
  - an old price more than six times the current one is treated as a data error and dropped (one
    beanie showed 89% off);
  - names that began with a stray trademark sign are cleaned;
  - photo files are split into files of at most 150 photos (51 files, the largest 1.5 MB, was 3 to
    5 MB per category), so opening a category on a phone loads far less;
  - on phones the 2D/3D switch sits beside the search box with short labels, so the sticky bar is one
    line shorter.

### Further upgrades found in the review (not done yet)
1. ~~**"New this week" has lost its meaning.**~~ Done in 2x: only the week's new picks carry it.
2. ~~**Weekly price refresh:**~~ Done in 2x (`tools/weekly_refresh.py`). re-run `shopify_pull.py`, `sitemap_sweep.py` and `sweep_filter.py` weekly
   to update prices, stock in his size and `hist`, so "Price drop" tags and the shortlist's
   "Down £x since saved" work across all 7,155 picks; drop picks no longer listed.
3. **Shop-by-budget sets:** £60, £100 and £150 buttons on Outfits using the builder's suggester.
4. **Size check per shop:** store size charts for the main shops and show what L means at each.
5. **Fit filters for the new shops:** about half the new-shop picks have no stock-by-size data; a
   browser pass over just those product pages could confirm his size.
6. **Duplicate colourways:** 53 shop-and-name pairs repeat (same product, colour not in the name); the
   lists already show at most two, but the sweep could add the colour from the variant.
7. **Blocked shops:** about 30 shops still refuse automated requests from the cloud; running
   `tools/browser_sweep.js` from a home computer would add them.

## 2x. First weekly refresh (6 Oct 2026)

A repeatable weekly refresh (`tools/weekly_refresh.py`, steps in `REFRESH.md`) checked every pick
against its shop, removed what is no longer sold, added new picks and published the result to the
artifact and to GitHub Pages. Totals: **7,525 picks** (was 7,155) and **575 outfits** (was 572).

- **Price check:** 6,626 picks were checked against the live listing (Shopify feeds, product pages,
  and headless Chromium for 128 pages that refuse a plain request). 17 prices went down and 50 went
  up, mostly sales that ended at Matalan, Clarks, Tu and M&S. The cards show "Price drop" and a price
  history.
- **Currency guard:** shops geolocate the cloud server and sometimes answer in dollars or euros (one
  run showed 1,527 false price rises). Every request now asks for the UK market, answers in another
  currency are retried, and a shop whose prices all move by one shared factor is left alone and
  reported (this week: Peacocks; Ted Baker, Colorful Standard and Rains answered only in other
  currencies).
- **Removed (63):** 14 sold out in every size, 34 sold out in his size, 2 Moss slim-fit trousers,
  and 13 things that are not clothing (tie-down straps, bivvy and survival bags, laptop sleeves,
  magazine rigs). Eight 6E safety boots stay listed as "his size sold out" watch items.
- **Moss data fixed:** Moss pages carry data for a dozen recommended products, and the old reader
  took the cheapest of them, so Moss picks had wrong names and prices (a "£4.95 linen shirt"). The
  reader now uses only the page's own product; 19 Moss picks were renamed from their pages.
- **Workwear rules enforced:** the October sweep had tagged items Workwear on looser rules (60%
  cotton, any boot, any shop). Following Emma's rules, the Workwear tag came off 67 T-shirts, 19
  safety boots that are not EE or wider, 23 trousers that are not black or charcoal, stretch,
  Cordura or not confirmed cotton, and about 110 fashion pieces from mixed shops (sunglasses,
  wallets, band tees, Boss blazers). They stay in their other styles. Work gloves, beanies, socks,
  base layers and the like keep the tag. 79 Workwear outfits were mended to match and 11 that could
  not be were dropped.
- **New picks (433):** 414 from 110 Shopify shops and 19 from shops read through their sitemaps,
  up to 6 a shop and 2 a kind, reduced first, all in his size with a photo. The filter learned new
  rules from this week's review (women's "W" items, swim caps and briefs, feed codes in names,
  muscle fit, Workwear: no T-shirts, black or charcoal trousers only, no stretch, Cordura or
  bundles, light colours out). Only these carry "New this week" now.
- **Outfits:** 22 outfits that lost a piece got the closest live match (same kind, shop and colour
  first; single-shop outfits stay single-shop), and 14 new outfits are built on the new picks.
- **Not checked from the cloud:** ASOS (195 picks), Ted Baker, Colorful Standard, Rains, Peacocks,
  M and M Direct, WoolOvers, Schuh and a few others refuse cloud servers or answer in another
  currency, even in a real browser. Their picks keep last week's price. The full list is in
  `data/refresh-report.json`.
- **Published:** the claude.ai artifact <https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2> and
  GitHub Pages <https://emmachilds98-wq.github.io/Wardrobe/> (the site is built into `docs/`, and
  the root `index.html` opens it).

## 2y. A better 3D model (6 Oct 2026)

- **Smooth body and clothes:** the torso, neck, arms, hands (with thumbs), legs, nose and shoes are now
  smooth tubes through tapered cross-sections (`secGeo` in the page), so there are no ball joints or
  seams at the knees, elbows or shoulders. Every garment is built the same way over the body with ease
  for its layer (shirt, knit, jacket), and puffers and parkas get extra loft.
- **Clothes fixed:** long coats hang from the shoulders to the knee (they used to float as a separate
  skirt); open jackets, cardigans and gowns now open at the front (the gap was at the sides); garments
  hang straight from the hips; an open shirt sits over a tee; front details of a hidden layer (buttons,
  pockets) no longer show through; short-sleeve and cuff hems only show on the outermost sleeve; trousers
  follow the calf so no skin shows at the knee.
- **Head:** a jaw, chin and brow shape, eyes with whites, irises and lids, brows, a slimmer moustache,
  a thicker neck, and hats (beanie, cap, bucket hat with a sloping brim) that sit on the hairline with
  the curls tucked under them. Sunglasses have two lenses and arms.
- **Shoes:** a shoe shape on its own sole (white or gum for trainers), laces on top, boot shafts, toes
  turned out a little.
- **Accessories:** the crossbody bag strap runs over the chest to a bag at the hip, backpack straps over
  the shoulders, belts with a buckle, a watch on the wrist.
- **Light:** filmic tone mapping and softer shadows.

## 2z. Shorter neck, more lifelike 3D model, and trousers that do not grip (6 Oct 2026)

- **3D model:**
  - A shorter neck: the head sits 2 cm lower and the neck is shorter and thicker, so the chin
    meets the collar as it should.
  - Hands have four fingers and a thumb.
  - Face tones are baked into the skin: light stubble on the jaw and upper lip, warmer cheeks and
    shade round the eyes.
  - Lash lines, ears with a rim and lobe, and a thin upper and fuller lower lip.
  - Soft contact shading on the body and every garment: inside the arms and legs, the sides of the
    chest, between the legs.
  - Jacket and coat shoulders sit lower and look natural, not padded.
  - Wide-leg and relaxed trousers are drawn with more room.
- **Trouser fit (Emma: Dave prefers trousers that do not grip):**
  - 51 slim, skinny and tapered trousers, jeans, joggers and shorts were removed, judged by name,
    our note or the shop's own description. "Tapered" only counts when nothing says the cut is
    loose (Stan Ray, Polar and Dickies loose cuts with a tapered leg stay), and cuffed joggers
    only go when they are slim.
  - 490 picks now carry a fit (wide leg, relaxed, straight or regular), shown on the card. They
    rank higher, the builder's suggestions prefer them, and new outfits use them first.
  - A "Trouser fit" filter under Filter shows regular, relaxed or wide only, or wide leg only.
  - 52 outfit pieces were swapped like for like (jeans for jeans, chinos for chinos, cords for
    cords), and one outfit with slim suit trousers was dropped.
  - The weekly refresh applies the same rule (`weekly_refresh.py fit`, and in `check`), and
    `sweep_filter.py` leaves tight fits out of new picks and labels the loose ones.

## 2za. Dave's face from his photos (6 Oct 2026)

- **3D face, matched to the photos Emma shared:**
  - The skin, beard and hairline are painted onto the head as a texture: fair skin with warm
    cheeks, and his short ginger-brown beard drawn as hairs along the jaw, chin and sideburns,
    with clear cheeks above it. The beard adds a little depth to the jaw.
  - A brow ridge and a fuller mouth area give the face its depth from the side.
  - Blue-grey eyes with a pupil and a darker rim, slightly hooded lids and a lower lid, under
    straight, thick dark-brown brows.
  - A longer, straight nose with a narrow bridge, a rounded tip and nostrils.
  - The moustache is one full ginger-brown chevron drawn as hairs, covering the upper lip, its ends
    drooping just past the corners of the mouth.
  - His curls are corkscrew ringlets in two browns over a dark-brown base: more volume on top, a
    few curls over the forehead, over the tops of the ears and short at the nape. Under a hat, only
    the curls below the brim show.
  - A slight closed-mouth smile, and warmer skin to match.

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

### Step 4b: Features suggested for next round
1. **Shop-by-budget sets:** "£60 / £100 / £150 outfit" buttons that run the builder's suggest engine
   over the photo-backed picks and show the set as a flat lay.
2. **Price-drop alerts on the shortlist:** re-run `shopify_pull.py` weekly for the shops behind
   saved picks and set `prev` and `hist`, so the shortlist's "Down £x since it was saved" lights up.
3. **Size check per shop:** store each Shopify shop's size-chart page and show "L at this shop is
   a 42 to 44in chest" on the card; flag shops that run small.
4. **Outfits from the new picks:** generate outfits per style from the 4,282 new picks, using
   only pieces with photos, so every outfit shows a full flat lay.
5. **Non-Shopify shops:** M&S, Next, Uniqlo, ASOS and the other big shops are not on Shopify; a
   headless-browser pass (`tools/browser_fetch.js`) over their sale pages would add them.

### Step 5: More stores to add next
These are in the directory but still have no picks: Gap, Levi's, Dr Martens direct, Vans,
New Balance direct, Timberland direct, Berghaus direct, Urban Outfitters, Pull&Bear, Bershka,
TK Maxx, BrandAlley, Very and F&F. The search index had only old or US prices for Gap and Levi's
this round. Check them again when they can be reached directly. Next round: aim for 3 to 5 picks each, and favour sale stock and
pieces that slot into existing outfits.

## 4. Product review and large-scale plan (6 Oct 2026)

The full review, with the render-against-photo comparison, the roadmap drawing and a tracker, is
in Emma's doc "Dave's Wardrobe: product review and upgrade plan":
<https://claude.ai/artifact/Ltsoegoei9Yj6XSf6NhgQV>. This section is the working copy for the
sessions that carry it out. Line numbers are `page.html` at commit 9e3f504.

### What the review found
- **3D clothes:** 12 fully photographed outfits were rendered beside their shop photos. Every one
  had at least one piece a shopper would not recognise. The repeating faults:
  - wrong colours (a sky-blue denim jacket, near-white stone chinos, white brown trainers);
  - one jacket cut and length for every jacket;
  - missing hoods;
  - boots drawn as low shoes;
  - patterns guessed from words;
  - a skin gap under hoodies;
  - a tiny floating tie;
  - one sunglasses shape.
- **Why:** every top is one torso tube (`make3D` 2385–2608). The only differences are hem height,
  sleeves and a few add-ons. Ease is fixed per layer (2516). Trousers vary only below the knee (2500).
  Inputs are just shape, palette colour, two photo-sampled colours (`TRUE`, `sampleCol` 1850–1883)
  and about 20 name regexes. Pattern UVs are stretched about 3.4:1 (2347).
- **Data:** 7,474 picks, 200 shops, 574 outfits; 95% of prices checked on 6 Oct.
  - Colour: no colour field.
  - Fit: stored for only 6.6% of picks.
  - Fabric: stored for 32%, but 97% of those are cut off by the lazy regex in
    `tools/sweep_filter.py` `fabric_of()` (line 175–176). That breaks the "100% cotton" filter:
    42 matches against about 1,149 real ones.
  - Offline catalogues (`cat/`, 5,860 picks matched) do hold fabric (58%), fit words (42%),
    prints (38%), closures (36%) and pockets (32%), with about 5 images per product.
- **2D:** 609 of 2,333 drawn pieces (26%, in 71% of outfits) misrepresent the product. The shared
  colour sampler treats tan, brown, rust and camel cloth as skin (1863). The board lost its
  background when it became a button: `.fit > svg` at line 94 no longer matches.
- **Page:** opening Shop downloads 17.7 MB (about 10.5 MB compressed). Search matches substrings
  ("red" finds Fred Perry). Builder suggestions ignore formality. The refresh can delete saved or
  owned picks. No page `lang`; Back does not move between views.

### Order of work
1. **Quick fixes:**
   - Belts are hidden in all 55 belted outfits: draw them over the top, or tuck the shirt when a
     belt is worn (belt band vs untucked hem at y 0.99–1.03).
   - Always put a tee under a shirt. In barrel-chore, ox-open, ramsey-weekend and x11-passenger
     the tee covers the shirt.
   - Stop "button-down" matching `/down/` (22 picks become puffers).
   - Gilets are plain unless the name says quilted (`texOf` 1226; "diamond" draws as quilt lines,
     2275).
   - "Longline" tees keep short sleeves.
   - Hoodie drawcords take `col2`.
   - Draw pocket squares.
   - 2D: board background (`.fit .board-btn svg`), dark-mode contrast, and Dave's new face (beard,
     chevron moustache, blue-grey eyes, straight brows, longer nose, curls with volume on top).
2. **Colour you can trust:** fix `sampleCol`. Only filter skin when a person is in the photo,
   crop to the garment on model shots, fall back to the name's colour when the two disagree,
   store colours in the data, and allow a manual override.
3. **Read the data we have:**
   - Fix `fabric_of`, backfill from `cat/`, regenerate the notes, and add a test.
   - Store structured details: colour option, composition, gsm, fit, length, rise, leg opening,
     closures, pockets, prints, images, measurements in his size.
   - Add data checks to `build_site.py`.
   - Keep saved and owned picks as watch items instead of deleting them.
4. **Faster page:**
   - Load photo packs per screen; save a 720 px photo for the large view.
   - Merge Dave's curls and give them a level of detail. They are 432k of the roughly 0.5M
     triangles in a frame.
   - Build the body, head and hair once and swap only the garments.
   - Pre-render card images at build time, which ends the double render (2767).
5. **3D phase 1, product specs:**
   - About 45 archetypes.
   - `data/specs.json` with archetype, fit, length, collar, closure, pockets, hems, zone colours,
     pattern, fabric and measurements, each with its source and a confidence.
   - A vision-labelling pass over contact sheets for the roughly 1,500 outfit pieces.
6. **3D phase 2, engine and body:**
   - Move from Three.js r128 to r160+. It is a module import; `encoding` becomes `colorSpace`
     (the `if(T.sRGBEncoding)` guards at 2278, 2314, 2321, 2614 and 2649 would silently skip
     sRGB); drop `convertSRGBToLinear` in `C()`; lights need about ×π.
   - Dave as a rigged CC0 base mesh built to his measurements, with three poses.
   - Use meshopt rather than Draco or KTX2, since the WASM decoders may be blocked in the
     artifact.
7. **3D phase 3, garment templates:**
   - Built in headless Blender (download.blender.org is reachable): pattern pieces draped on
     Dave's body with cloth simulation, then baked.
   - Morph targets for length, ease, sleeve, hem, leg width, taper, rise and crop.
   - Switchable parts: hoods, collar types, plackets, zips, pockets, hems and linings.
   - UVs in real units.
   - About 8 MB in all, loaded per archetype.
8. **3D phase 6, footwear and accessories:** 15 shoe lasts with sole, upper, lace and trim zones;
   accessory variants by style.
9. **3D phase 4, fabrics and photos:**
   - About 25 CC0 fabric sets (ambientCG, Poly Haven).
   - A stripe and check shader driven by the measured colours and spacing.
   - Packshot photos warped onto the template's front panel.
   - Shoe side photos projected onto the shoe sides.
10. **3D phase 5, fit and layering:**
    - Garment minus body measurement sets the morphs (chest ease: under 8 cm slim, 10–16
      regular, 18–26 relaxed, over 28 oversized).
    - A distance-field push-out for layers.
    - Rules for tucks, hoods over collars, and boots.
11. **3D phase 7, weekly check:**
    - Render each item at its photo's angle and score outline overlap and colour Delta E against
      the cut-out photo.
    - Proposed gates: overlap 0.8 or better, and Delta E 5 or less, for 90% of outfit pieces.
    - Send failures to a review sheet.
    - Add an approve/reject page for each week's changes.
12. **Page upgrades alongside:** search, builder rules shared with `make_outfits.py`, phone
    navigation and deep links, size confidence from size charts and the measuring card,
    accessibility, budget sets, and his wardrobe with photos and a wear log.

### Needed from Emma
- Dave's measurements: chest, waist, hips, inside leg, shoulder width and sleeve length. Also
  confirm 1.83 m and the 15.5–16 in neck.
- A decision on the cropped reference photos. Either a permission rule lets them into the repo,
  or they stay private elsewhere.
- A yes to the newer Three.js and the Blender templates.
- Which step to start with (recommended: 1 to 3).
