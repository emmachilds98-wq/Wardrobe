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
