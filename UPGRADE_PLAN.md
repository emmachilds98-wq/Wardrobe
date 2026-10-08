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

## 2zb. Edit Dave, no beard, and a better fit (6 Oct 2026)

- **Edit Dave:** a character editor with a live 3D preview. Open it from Page settings, from the 3D
  view of any outfit, or from the builder. It sets:
  - Height (160 to 200 cm) and build (slim, regular, broad).
  - Skin tone.
  - Hair colour, length (short, ear, collar), curl (loose, curly, tight) and volume.
  - Moustache style (chevron, walrus, handlebar, pencil or none) and colour.
  - Beard (none, stubble, full).
  - Eye colour and brows.

  Saving re-renders every 3D figure. Emma's saves are stored in the page's shared data, so
  everyone sees the same Dave. Other viewers keep their changes in their own browser only.
  "Back to his defaults" resets everything.
- **Defaults:** no beard; the ginger-brown chevron moustache stays.
- **Fit:**
  - Sleeves have a rounded head that runs into the shoulder seam, so no square shoulders,
    pads or gaps.
  - Sleeves are less baggy. Short sleeves sit just off the arm.
  - The trouser rise covers the seat and crotch.
  - Knit hem ribs follow the body's shape.
  - Collars sit lower and lean in.
  - A belt under an untucked top is hidden.
  - The hair stays inside the jawline, so nothing reads as a beard.
  - The lighter curls are a warm chestnut, not grey.

## 2zc. 3D views that keep working, a fuller Edit Dave, and clothes that sit better (6 Oct 2026)

- **Fix: the outfit view's 3D model stopped loading after editing Dave.**
  - Each turnable view (outfit view, builder, Edit Dave) made its own WebGL context and never freed it.
  - Phones allow only a few per page, so after some views (or Edit Dave opened over an outfit) the next
    one failed and stayed on "Loading the 3D model…".
  - Now all of them share one renderer. Edit Dave borrows it from the outfit view and hands it back
    when it closes, and a hidden view does not draw.
  - If the browser drops the 3D context anyway, the view says so and offers "Try again". The card
    renderer recovers on its own.
- **3D views:**
  - Front, Side, Back and Turn buttons, and Full, Top and Face framing.
  - Scroll or pinch to zoom, and arrow keys to turn.
  - Tap a garment to see what it is and its price. In the outfit view, the matching photo card is
    picked out too.
- **Edit Dave:**
  - Body, Face and Hair tabs. The preview frames the part being changed (whole figure, face, hair).
  - New options:
    - shoulders (narrow, average, broad) and middle (flat, average, fuller), which the clothes follow
    - face shape and nose size
    - glasses (none, round, square) with frame colours
  - Undo, one step per change, and "Try another outfit" to check the look on other clothes.
- **Clothes on the model:**
  - Trousers fold in soft rings above the shoe and crease behind the knee. Long sleeves bunch at the
    wrist and crease at the elbow.
  - Untucked shirts have a curved hem, and polos have short side vents.
  - Shirts worn with a blazer, waistcoat, tie or suit trousers are tucked in, with the belt showing.
  - Shirt cuffs with a button, and a cuff edge on blazers and coats.
  - Belt loops on trousers, back pockets, a coin pocket on jeans, and a drawcord, ribbed waist and
    cuffed ankles on joggers.
  - Sleeves under a long-sleeved layer are left out, so they never poke through.
  - Shoulders slope naturally under clothes instead of puffing.
  - Leg shading blends into the hips, so no light patch shows at the crotch.

## 2zd. 2D drawing fixes (6 Oct 2026)

- **Fixed: 2D clothes had lost their colours and textures.** A helper added for the 3D hair colour
  shared its name with the 2D drawing's colour function and replaced it, so every garment was drawn
  in plain near-black. It is renamed, and no other function names clash.
- **2D head:**
  - The curls on top sit lower, closer to his head as in his photos.
  - The head, hair and hats are drawn 8% smaller against his body, scaled about the chin so the
    neck still meets it.
  - The face itself is unchanged.

## 2ze. A real human body for the 3D model (6 Oct 2026)

- **The body:**
  - Dave's 3D body is now the MakeHuman base mesh, a professionally sculpted body released under
    CC0 by the MakeHuman project.
  - `tools/build_body.py` reads the asset files itself (no MakeHuman program code) and makes him a
    tall, slim young man.
  - It poses him relaxed: arms by his sides, elbows soft, backs of the hands out with the fingers
    loosely curled, feet under the hips.
  - It writes `data/body.json` (about 770 KB). `build_site.py` copies it next to the page.
  - Re-run with `python3 tools/build_body.py`; it downloads the assets on first use.
- **Edit Dave on the real body:**
  - Build, shoulders, middle, face width and nose size are now real shape targets on the mesh.
  - Height still scales the whole figure.
- **Face:**
  - The detailed MakeHuman head, with real ears, eyelids, lips and nose, and a slight lift at the
    corners of the mouth.
  - His eyes sit in the sockets: white, iris and pupil in his eye colour, a clear wet cornea that
    catches the light, and a lash line.
  - The brows, moustache, glasses and sunglasses are placed from a depth map of his face.
  - The curls and hats hang from his measured skull.
  - Skin is coloured per vertex: warmer cheeks, nose tip and ears, lips, the stubble or beard
    option, and the scalp tinted under his hair.
- **Clothes:**
  - Built through cross-sections measured from the real body, so they follow his shape.
  - Tops hang straight from the chest rather than pinching in at the waist.
  - Collars and necklines sit on his real neck.
  - Skin under clothes is left out by body region (chest, arms, hips, thighs, shins, feet), so
    nothing pokes through.
- **Fallback:** if `data/body.json` cannot load, the page uses the older hand-built body.
- **Removed:** the "What to wear today" section of Outfits. The rest of the Outfits area is
  unchanged.

## 2zf. A more natural, more human 3D Dave (6 Oct 2026)

- **Moustache fixed:** it sat below the mouth because the face measurements picked each feature one
  step too low. The script now walks down the face profile feature by feature (nose tip, under the
  nose, upper lip, the line between the lips), so the moustache and lip colour sit in the right
  place.
- **Moustache and brows as hair:**
  - The moustache is now about 1,500 fine hairs rooted on the upper lip, in three shades of his
    moustache colour. Each style changes the root area and how the hairs lie: chevron, walrus,
    handlebar (ends turned out and up) and pencil.
  - Brows are about 150 short hairs, thicker and pointing up at the inner end, lying outwards along
    the rest.
  - Real eyelashes along the upper lids.
- **Expression:** a relaxed, friendly face from MakeHuman shape targets:
  - mouth corners lifted, soft laugh lines, slightly fuller cheeks;
  - a little more upper-lid fold, so he looks relaxed rather than staring.
- **Shape:** a more masculine torso (a little more chest, a straighter waist, narrower hips).
  - Tops hang straight down from the widest part of the chest with a slight taper, never following
    the waist in, so there is no hourglass.
  - Necklines follow his shoulder line up to the neck, crew necks dip at the front, and collars sit
    on top. Nothing pokes through and nothing rides up the back of the neck.
- **Skin:**
  - Contact shading baked into the body: creases, eye sockets, nostrils, ears, between the fingers,
    armpits and inner thighs.
  - A touch of warmth in the shadows, faint shadow under the eyes, and slight natural colour
    variation.

## 2zg. Precise body and face sliders in Edit Dave (6 Oct 2026)

- **Slimmer default:** the default build is a little slimmer: less added chest and waist, a flatter
  belly, slightly less cheek volume. Tops on the real body no longer have the old minimum widths
  below the waist, so they follow a slim body.
- **Sliders:** every shape option is now a slider from -1 to 1, blending real MakeHuman shape
  targets. `tools/build_body.py` bakes a pair of targets for each.
  - **Body:** weight, muscle, shoulders, chest, waist, belly, hips, arms, legs and neck, plus height
    and skin.
  - **Face:** face width, jaw, chin, nose, lips, ears, eye size and expression (serious to bigger
    smile).
- **Editor:**
  - Each slider shows its value in words ("Slimmer 50%") with a Reset link.
  - Quick body types: Dave, Slim, Average, Athletic, Heavier.
  - A live line gives his estimated chest, waist and hips in inches from the model, as a rough
    sizing guide.
- **Fitting to the sliders:**
  - Clothes re-measure for every slider position.
  - Each slider also moves the face landmarks (eyes, ears, skull, mouth).
  - The page re-measures the front of the face for the current shape, so brows, lashes and the
    moustache stay on the skin.
- **Older saves:** the earlier fixed choices (build, shoulders, middle, face, nose) are converted to
  slider positions automatically, including the copy shared in the page's data.

## 2zh. Moustache, brow and hair controls, proportions, face detail, layering (6 Oct 2026)

- **Moustache sliders:** position (up or down), depth (closer to or further from the skin), width,
  hair length, thickness and ends (turned up or drooping), for any style, to fix placement by eye.
- **Brows:** a colour (match his hair, swatches or any colour), thickness, height, arch, angle and
  length.
- **Hair:**
  - Styles: his curls, a short crop, straight and swept back, a buzz cut, or bald.
  - Highlights and grey (salt and pepper).
  - Hairline (lower to receding) and the curls over his forehead.
  - Length, curl and volume where they apply.
- **Proportions:** leg, body, arm and neck length, and head size.
  - His total height stays the same, and the size line now includes his inside leg.
  - The model is built at standard proportions, then one pass stretches heights band by band (feet
    unchanged) and re-hangs the arms from the shoulder. Body and clothes go through the same pass,
    so they always line up.
- **Face detail:**
  - Fine skin pores from a bump pattern in the skin shader.
  - Real irises: fibres, a lighter ring by the pupil and a darker rim, on a curved cap.
  - Eyeballs shaded under the upper lid and at the corners.
  - A crisper lip edge and a mouth line.
  - Deeper shading in the face's creases, and a little more contrast in the light.
- **Layering:**
  - The skin at the base of the neck is hidden by direction: it stays at the front, where necklines
    dip, and goes at the sides and back, where it showed through.
  - Under sleeveless tops the shoulders stay bare, and gilets, vests and waistcoats slope at the
    shoulders instead of forming a flat shelf.
  - A hoodie's hood lies outside an open coat or jacket worn over it.
  - Overshirts, chore jackets, shackets and flannels layer over a tee or polo rather than under it.

## 2zi. Hair for his curl type, face from his photos, neck layering (6 Oct 2026)

- **Hair editor, his hair type only:** loose curls with ringlets. The bald, buzz, straight,
  receding-hairline and grey options are gone; saved settings that used them fall back to his cut.
  - Base style: his short cut from the photos, with curls over the forehead to just above the
    brows and fuller sides above the ears.
  - Other styles he could grow: short sides with a curly top, a closer crop, curls swept back,
    grown out, and longer curls.
  - A brown scale (dark to light brown), sun-lightened ends, length, volume, curl (looser waves to
    tighter ringlets) and how far the curls fall over the forehead.
  - Each curl is a small clump of fine strands, darker at the root and lighter at the tip.
- **Face, from his photos:** blue eyes, straighter brows, a ginger-brown moustache only (no
  beard), a friendlier smile and light freckles over the nose and cheeks (with a slider). The
  scalp tint follows the hair shade.
- **Layering at the neck:** skin is hidden only where the clothes cover it. Neck and shoulder
  skin that ran out over the shoulders is removed at any height. Behind the neck, skin is removed
  only below the collar line, so the back no longer shows gaps or jagged edges.

## 2zj. Moustache placement (6 Oct 2026)

- The nose-base landmark sits about 4mm below where the nose meets the lip, so the moustache started
  low and its hairs hung over the mouth.
- The roots now start right under the nose and fill the upper lip. Each hair falls to about the lip
  line (the walrus a little past it), and the hairs lie along the curve of the lip instead of
  standing out from it.
- The pencil style is now short and trimmed, from under the nose to just above the lip.
- This is the starting position. Placement saved against the old position (up/down and depth) is
  reset once, so it starts from the new one.

## 2zk. His saved look as the base, more hair and cut options, hairline fix (6 Oct 2026)

- **Base model:** the look the owner saved in Edit Dave is now Dave's built-in default (`CHAR_DEF`), and "Back
  to his defaults" returns to it.
- **Sliders centred on him:** every slider has his saved value in the middle.
  - Each end still reaches the slider's full range. Where his value sat near one end, that end reaches a little
    further, for example leg length now goes from -1.6 to 1.
  - The stored value is the real one, so existing saves load unchanged.
- **Cut:**
  - Two new styles: short back and sides (tapered), and curly top with faded sides.
  - Sliders for the top, sides and back.
  - Sides and back can be natural, tapered or faded.
  - Hair cut close shows as a short tint on the scalp, fading to skin for a fade.
  - Sideburns stay short in every cut.
- **Curls:**
  - Curl size and finish (defined ringlets to softer and fluffier).
  - Which way the curls fall.
  - Length of the curls over the forehead.
- **Hairline:**
  - The short cuts keep his own hairline. The old short hairline was high at the temples and read as receding.
  - His hairline now has short sideburns in front of the ears and a proper temple line.
- **Forehead clipping:**
  - The hair now sits on a map of his real head shape (`headRad`), measured from the body mesh, instead of a
    fitted egg, so the hairline meets the forehead cleanly.
  - The curls over his forehead root on the hair at the hairline. The old ones took their depth from a face map
    that stops below the hairline, so some floated or sank.
  - Any curl that would pass through bare skin is tipped outward, or left out.

## 2zl. His current look as the base, defined curls, more curls on the forehead (6 Oct 2026)

- **Base:** the owner's second save is now Dave's built-in default (his "current" look). Every slider has it in
  the middle, as before.
- **Defined curls:**
  - Each curl is now a lock: a bundle of fine hairs following one spiral, full at the root and gathering to a
    point at the tip.
  - This matches the loose but defined ringlets in his photos, where the old version had two or three wiry
    strands.
  - "Finish" runs from tight, defined locks to splayed, fluffy ones.
  - The spiral is smoothly sampled, and the hair has about twice the old vertex count (about 770k), so it still
    builds in well under 0.1 seconds.
- **Forehead curls:**
  - Gentler S-shaped locks lie along the forehead, flattened against it, and fall toward the brows.
  - Their slope comes from his real head shape, not the fitted egg, which tipped them forward.
  - They start a lock's thickness off the skin.
  - The "Curls over the forehead" slider now allows up to about 50.
- **Sliders:** with his current values in the middle, the curl, curl size, finish, length, top and forehead-curl
  sliders reach further than before.
- **Hair base:**
  - It now includes the nape (the head-shape map takes in the top of the neck).
  - It rises out of the skin more gently, so a bare hairline (curls pushed back) has a smooth edge.

## 2zm. Hair that matches top to forehead, stronger sliders, clothes on his real shape, scarves (6 Oct 2026)

- **Base:** the owner's save (unchanged since 2zl) stays the base, with every slider centred on it.
- **Forehead curls:**
  - They are now the same ringlets as the rest of his hair, not a separate flatter lock.
  - They hang down the forehead's own slope toward the brows and stop above them.
  - Each is turned so its spiral swings away from the skin.
- **Top of the head:** curls on top tumble forward over the head (and down over the crown) instead of standing
  straight out.
- **Sliders:**
  - Curl runs from waves (under a turn) to tight ringlets (about three turns, narrower).
  - Curl size changes each lock's width, its hair thickness and the number of hairs in it.
  - Finish runs from defined (tight bundle) to fluffy (splayed).
  - Every hair slider keeps a full step either side of his base.
- **Clothes:**
  - The chest, shoulders and upper back of every top now follow his own body shape, pushed out by the cloth's
    thickness. Below the chest they blend into the straight hang.
  - The hollows (between the pecs, under the arms) are bridged.
  - The neckline is cut cleanly along a line, open fronts line up with the opening below, and stripes and knit
    run on without a seam.
  - Collars stand round the neck with a flared foot. Shirt collar points lie on the chest. Blazers and coats get a
    collar round the back of the neck.
  - Pockets, plackets, zips and lapels are placed on the clothes as built (by casting rays), not on a guess.
  - Gilets, vests and waistcoats keep their sloped shape.
- **Scarves:**
  - The loop sits on the outermost collar, measured from the clothes around the neck.
  - The two ends lie down his front over whatever he wears, one longer, with fringed ends.
  - Shirt collar points tuck away under a scarf.

## 2zn. Proportions from his photos, body controls, tops that fit (7 Oct 2026)

- **Proportions:**
  - The saved base had his legs at 44.9% of his height (shorter than nearly all men) and a large head.
  - His photos show a slightly long body, nothing marked, so the base is now legs at 46.6% of his height (most men
    are 46 to 49%) and 7.8 heads tall.
  - Older saves take these new proportions once (`propV`).
- **Proportion sliders:** they keep a set span either side of him (legs 45.5% to 47.6%), so they adjust him
  without throwing him out of proportion.
  - Leg length trades against the body, so his height stays the same.
  - A line under them gives his leg-to-height share and head count against the usual range.
  - "His proportions" and "Average man" buttons set all five lengths at once.
- **New body sliders:**
  - shoulder slope (squarer to more sloped, with the arms following);
  - body depth front to back;
  - how clothes fit, from slimmer and closer to looser and straighter.
- **Tops:**
  - Hems are set from his crotch, as real ones are: a tee or polo covers the waistband, a shirt is a little
    longer, and a blazer covers the seat. Before, they ran below the crotch.
  - Below the chest they take in toward the waist by the fit slider.
  - Sleeves stop under the shoulder cover, so the shoulder rounds over the arm instead of forming a square pad.

## 2zo. Lean build from his photos, legwear on his real legs, cloth that drapes (7 Oct 2026)

- **Build:** his photos show a tall, lean man, with a slim chest and arms, moderate slightly sloped shoulders, a
  flat stomach and slim legs.
  - The base is now: weight -0.35, muscle -0.25, shoulders -0.15, chest -0.35, waist -0.1, belly -0.25, hips
    -0.15, arms -0.3, legs -0.3, neck -0.15, shoulder slope 0.3, body depth -0.15.
  - Older saves take this build once (`propV` 3).
- **Shorts and trousers:**
  - Each leg follows his own thigh, knee and calf (centre and size). The old fixed legs sat 3cm behind his thighs.
  - Below the thigh the leg hangs nearly straight; shorts flare slightly to the hem.
  - The seat rounds under at the crotch, so there is no flat panel or bump.
  - Ankle folds are softer.
- **Tops:**
  - The chest and shoulders lie like a sheet: pec and rib shapes are smoothed out, but the cloth never comes
    closer to the skin than a few millimetres.
  - The lower edge and the arm edge are cut cleanly, with no jagged lines.
  - Thick layers stand off the body less than their full thickness, and less again over the shoulders, so coats
    and jumpers no longer look padded. Each layer still sits outside the one under it.

## 2zp. His saved dimensions as the base; socks, shoes, lapels, cleaner openings (7 Oct 2026)

- **Base:** every value the owner saved (body, proportions, face, moustache, hair) is now Dave's built-in default,
  and every slider is centred on it.
- **Socks:** with shorts he wears ribbed crew socks with a cuff a little way up the calf. They are white, or black
  with dark shoes, and the skin under them is hidden.
- **Shoes:**
  - Trainers: a two-tone sole (midsole and outsole), a toe bumper, a heel tab, a padded collar and a side panel.
  - Dress shoes: a slimmer, lower toe, a thin sole with a heel block, and a welt.
  - Boots: a lugged sole, a shaft sized to his ankle, and a pull tab.
- **Lapels:**
  - Blazers and coats have real lapels lying on the jacket, widening from the top button to the notch under the
    collar.
  - The outer edge is rolled and has a darker edge line.
- **Open fronts:** jackets, cardigans and coats are cut cleanly along the opening, as the neckline is, with no
  ragged notches by the collar.
- **Shoulders:** the sleeve top sits fully under the shoulder cover, so the seam is a clean line.

## 2zq. Drag along him when zoomed; trousers as one piece; product details (7 Oct 2026)

- **Drag when zoomed:**
  - In every 3D view (the outfit view, the builder and Edit Dave), once zoomed in, dragging up or down moves along
    his body, from face to feet in a stroke or two. Dragging across still turns him.
  - The direction is decided by the first few pixels of the drag.
  - The view stays within his height, and recentres when zooming out or pressing Full, Top or Face.
  - Up and down arrow keys also work.
- **Trousers and shorts:**
  - The hips, seat and tops of the thighs are now one piece of cloth draped over him (`lowerWrap`).
  - Across the front of the crotch it lies flat from thigh to thigh.
  - The crotch seam hangs a little below his body.
  - Each leg carries on from it with no seam. Before, the separate rounded "rise" read as an underwear layer.
- **Product details from the photos:**
  - Jeans: gold topstitching down the outside seams, scooped front pockets and copper rivets.
  - Chinos and tailored trousers: slanted front pockets.
  - All trousers: the fly stitching lies on the cloth.

## 2zr. Clothes drawn from the shop photos and listings, in 2D and 3D (7 Oct 2026)

- **Reading the photo (`readLook`):** each piece's shop photo (already published with the page as a data URI, so it
  can be read pixel by pixel) is read once, when it loads, for the following.
  - Its main and second colour: the same method as before, with white-on-white photos and orange or rust cloth (once
    taken for skin) now handled.
  - Stripes (across or down) at their real spacing and colours, from how the brightness repeats down the rows and
    across the columns. They are trusted when the listing says stripe, or when they are very strong.
  - Checks and all-over prints, kept as a swatch of the cloth itself:
    - the square of the garment with the least skin or background in it;
    - lighting evened out so folds and shadows don't repeat;
    - mirrored into a tile so it repeats without seams.
  - The print, graphic or logo on the chest, cut out of the photo:
    - the cloth around it made clear;
    - its place and size on the garment recorded;
    - hands, bag straps, plackets and side folds left out.
- **Reading the listing (`descOf`):**
  - collar (button-down, band or grandad, camp or Cuban), neckline (henley...), zip, pockets, fit;
  - tipping, rugby stripes, pleats, turn-ups;
  - pattern words, print or logo words, the material, a second colour named in the name, and the brand.
- **3D:**
  - The cloth uses the real stripes, check or print, sized to the real garment; material sets the shine.
  - Graphics and logos sit on the chest as a patch following the cloth; known brands without one found get a small
    chest logo.
  - Twin tipping on collars, neckbands and sleeve ends.
  - Camp, band and button-down collars; henley plackets; full zips; chest pockets.
  - Oversized and slim fits (an inner loose piece never pokes through a closed outer one).
  - Pleats and turn-ups.
  - Three stripes on adidas trainers in the photo's second colour.
- **2D:**
  - The same photo stripes, checks and prints.
  - The real chest print in place of the old stand-in block.
  - The collar types and pockets.
  - From the 3D work:
    - crew socks with shorts (trainers and lace-ups only, not loafers, sliders or sandals);
    - three stripes on adidas trainers;
    - jeans' gold topstitching, scooped pockets and rivets;
    - chinos' slanted pockets;
    - pleats and turn-ups.
- **Trousers:** the crotch front lies flat across (no hollow "cup").

## 2zs. Never shirtless; zip up or unzip; the shop photo's own front; collar, layer and seam fixes (7 Oct 2026)

- **Never shirtless.** Six outfits put a jacket, fleece or gilet straight on his skin, and four had a lone shirt
  "worn open". Each now has a top under it:
  - The six Workwear outfits use **his work T-shirt**. That is a new kind of piece (`"own": "work"`) that he already
    has: the card says "Already his, nothing to buy", it adds nothing to the price and it never shows as "no longer
    listed". This follows the Workwear rule that work supplies his T-shirts.
  - The others get real picks. The fleece walk gets a Tog24 grey marl tee (£8), the Montirex outfit a Montirex black
    tee (£13.99), and the resort shirt a Saltrock white tee (£8). The crinkle shirt gets a Blue Inc ribbed tee (£6.99),
    the Yedra shirt a Luke 1977 Dovetail tee (£12) and the Luke 1977 outfit a Luke 1977 Ellison waffle tee (£13).
  - Notes and totals were updated.
  - The builder adds a plain white tee to the figure whenever a jacket, gilet, cardigan or waistcoat has nothing
    under it. It also says so, and an "Add a T-shirt" button picks a plain tee in his size and the chosen styles.
  - Suggest never leaves a cardigan on its own.
  - The weekly refresh adds a tee to any outfit that ends up bare: his work tee for Workwear, otherwise the cheapest
    plain neutral tee in style. It also leaves "own" pieces alone.
- **Zip up / Unzip** on the 3D model's view bar, whenever the outfit has a jacket, coat, blazer, gilet, cardigan or
  overshirt:
  - Done up, the piece shows a zip down the middle or a row of buttons (a blazer's one or two at the waist).
  - Coil zips take the cloth's colour; metal is kept for workwear, denim, leather, Harringtons and bombers.
  - A hoodie under a done-up jacket keeps its hood out over the collar. A hooded jacket (parka, "active" jacket,
    anorak) has its own hood on his back.
- **Gilets** are built like a jacket's body:
  - They cover his shoulders, with clean armholes cut at the point of the shoulder (no more zigzag where the top
    underneath poked through).
  - A zipped stand collar on bodywarmers.
  - In 2D a done-up gilet is drawn without sleeves, so the top under it shows at the arms.
- **Overshirts** (shackets, chore and work shirts, flannels) are worn open over a shirt or tee, as jackets are.
- **The shop photo's own front (3D).**
  - When the photo is a flat or ghost-mannequin shot of a closed top, the garment's front is cut out of it, from just
    under the collar to the hem. Background is made clear, the edges are feathered and the lighting is evened out
    smoothly.
  - The cut-out is laid over the front, so pockets, panels, plackets, prints and logos are as sold. Examples: the
    Luke 1977 Thor tee's ecru chest panel, the Admiral and Weekend Offender prints, and the Pacaya shirt's buttons.
  - The drawn pockets, plackets and logos then stand down, so nothing is doubled.
  - A photo is not used when:
    - it is worn by a model (his neck above the collar, a chin at the top middle, hands, or other clothes in the
      cut-out);
    - it is a folded shirt in its packaging (holes where the background shows through);
    - much of it is far from the garment's own colours.
  - A maker's neck label is no longer taken for a logo.
- **Sleeves** take their own colour where the photo shows them in another (raglan, colour-block). A
  "sleeve-stripe" polo gets stripes round the sleeves only, not across the body.
- **Colour:**
  - Charcoal and grey pieces are no longer crushed to near black (that pull-down is now kept for things the listing
    calls black or that read very dark).
  - A strong, even stripe is read from the photo even when the listing doesn't say stripe.
- **Trousers:**
  - Cut from the listing: slim, skinny, tapered (and cuffed joggers) narrow to the ankle; barrel legs are fuller at
    the knee; bootcut and flares widen at the hem; cropped and ankle-length end higher.
  - Where the legs meet the one-piece top, the cloth now runs on in one line: no shading step, specks or broken
    check across the thigh. Wide legs widen gradually from the hip.
- **Checked again** (the fixes from the last two rounds):
  - open shirts' collars at the sides;
  - no inner collar under a closed shirt;
  - hoodie under an open or done-up jacket;
  - the crotch;
  - yokes, seams, pockets and prints on the back;
  - shoe colours.

## 2zt. Shoulders, collars, vests, hoods, hems and colours (7 Oct 2026)

- **Shoulder clipping.**
  - *Cause:* the round sleeve tube met the body-shaped cloth over the shoulder in a zigzag, poking through it.
  - *Fix:* round the top of the arm the cloth now settles exactly onto the sleeve's own line, so the two meet in a
    clean seam on every top.
  - A vest's high back no longer shows through jackets and shirts worn over it.
- **Collars.**
  - Done-up shirts and polos have a real collar: a leaf that folds down from the stand all the way round the neck,
    shows at the back, and comes to its two points on the chest.
  - Open collars lie on the cloth point by point, instead of standing off the shoulder as flat fins.
  - Zip-up jackets, fleeces and track tops have a stand collar, lower and turned down when open, instead of a
    shirt collar.
- **Vests:**
  - **Built from the body.** They are cut from his body surface like the other tops, not from slices that rose into
    a high neck. The cut is read from the listing:
    - classic tank: narrow straps and a low scoop;
    - muscle or training vest: broad straps and deep armholes;
    - racerback: straps that meet behind;
    - vest top or sleeveless tee: crew neck, straps out to the shoulder.
  - **Knitted vests** (sweater vests, slipovers) have no sleeves and a V neck, in 3D and 2D, so the polo or shirt
    under them shows at the arms.
- **Hoods** worn down are soft cloth lying flat on the upper back:
  - thickest where they gather at the neck, thinning to the point at the shoulder blades, with a centre seam and a
    gathered rim round the neck;
  - under a jacket they lie out over it.
  - The rigid dome is gone, and hooded jackets use the same hood.
- **Shoes and trouser hems.**
  - Below the ankle bone the trouser leg falls straight on, instead of being stretched along the foot.
  - The hem rests on the shoe: higher at the front, falling to the heel, a little fuller and set back. The shoe no
    longer pokes through.
  - Cuffed joggers gather at the ankle, above the shoe.
- **Colours:**
  - **Named colours win.** The colour the listing names (the colourway after the comma or dash is read first; brand
    names like Pretty Green don't count) now wins when the photo reading is clearly off. Typical causes were a model
    in shot, another colourway photographed, or skin and background seen through a mesh.
    - Hue families agree at any depth (green covers olive and khaki greens; blue covers navy to sky).
    - Grey agrees at any shade.
    - Patterned pieces are left to the photo.
  - **Outfit colour as fallback.** With no colour in the name, the colour the outfit records for the piece stands
    in.
  - **Other photo-reading fixes:**
    - Trousers are read lower in the photo, where the legs are (a model's top is above), and caps near the top.
    - A shop's placeholder (a logo on a coloured card) is ignored.
    - A face at the top of the photo marks a model shot, so its front is not projected.
  - **Result:** over 300 listings, about 40 readings were corrected, among them the black mesh vest (it read as
    white), black bags and overcoats, the ASOS storm jacket and a blue cap that read as white.
- **2D:** shoulders on sleeveless pieces are rounded, not pointed. Knitted vests and done-up gilets are drawn without
  sleeves.

## 2zu. Phase 1 of the 3D upgrade: fitted tops, layering, trousers and weekly checks (7 Oct 2026)

Status: parts 1a (checks), 1b (tops) and most of 1c (trousers) are done; 1d (fitting room) is next.

- **Automatic 3D checks (`tools/check_3d.js`).**
  - Renders every outfit (or `--sample N`, `--ids a,b`) from the front, side and back, both as shown and as a
    flat colour-per-layer image. It flags:
    - skin or an inner layer showing through an outer one;
    - small see-through holes;
    - floating parts;
    - colours that drift from the listing.
  - It writes `report.json` and pictures of anything flagged. With `--report` it adds a `checks_3d` summary to
    `data/refresh-report.json`.
  - Usage: `node tools/check_3d.js --site docs --sample 80 --out qa [--debug]`.
  - Baseline over 80 outfits: 10 pokes, 76 with the trouser slit, 4 colour drifts.
- **Tops as one fitted piece (`fitTop`).**
  - Every top with sleeves is now one continuous piece of cloth, built from radial maps of his body (`fitMaps`):
    - the body bridges hollows and hangs straight from the chest, taken in at the waist as Edit Dave's fit says;
    - the yoke rounds over his shoulders at the cloth's thickness rather than its looseness, so jackets no
      longer look padded;
    - each sleeve grows out of its own armhole edge. The sleeve head rounds over the arm, and the cloth settles
      around the armhole, so there is no ledge, box or seam to poke through.
  - Sleeves photographed in another colour are tinted along a natural seam line, from under the arm to the point
    of the shoulder.
  - Vests, gilets and waistcoats keep their cut shapes.
- **Layering.**
  - What each piece leaves on him is recorded in maps (torso, shoulders, neck, each arm, legwear).
  - Every later piece is kept outside them across each row's whole height, so the edge of a ribbed hem or
    waistband underneath cannot come through. This applies to its body, sleeves, collars, cuffs, bands and
    plackets.
  - A tucked-in shirt goes under the trousers; an untucked top lies over them.
  - A closed gilet or waistcoat hides the pockets, plackets and cords under it.
- **Collars from the neckline (`fitCollar`).**
  - Crew neckbands, funnel and stand collars, shirt and polo collars (stand plus a leaf folded back over it) and
    coat collars grow up from the top's own neckline, so they never stand off it or sink into it.
  - They are built around a fixed line through the base of his neck, so they stand up instead of tipping forward.
- **Smaller fixes:**
  - The hoodie pocket lies on the cloth, with its two slanted openings.
  - Jacket pockets sit on the panel when the front is open.
  - The quarter-zip has a real funnel collar.
  - "Button-down" shirts are no longer treated as down-filled.
- **Trousers.**
  - The slit of light down the middle, front and back, is closed: where his thighs would touch, each leg's inside
    is pressed flat against the other.
  - Still to fix: a small gap right under the crotch on some trousers and shorts.
- **Speed.** Pockets, plackets and photo fronts are placed from a depth map of the clothes, not by casting rays,
  so outfits build as fast as before (about 0.1 to 0.25 s).
- **Next:**
  - Close the gap under the crotch.
  - Tidy the remaining small collar artifacts at the side of the neck.
  - Phase 1d: a fitting room in the Style guide, with Dave in plain underwear and the body sliders, opened from
    every outfit's Edit Dave button.
  - Run the checks over all 574 outfits, and hook them into the weekly refresh.

## 2zv. The fitting room, and fabrics read properly (7 Oct 2026)

- **Fitting room (Phase 1d):**
  - Edit Dave now opens in a fitting room, with Dave in plain grey boxer briefs and a dark waistband, so his
    build and proportions are easy to judge against the body sliders. An "In an outfit" switch puts the clothes
    back on, and "Try another outfit" moves through the outfits.
  - It opens from every outfit's "Edit Dave (fitting room)" button, and from a new Fitting room section in the
    Style guide.
  - The briefs and waistband are lifted straight off his skin. The copies of each vertex along the body's
    region seams are welded, so the cloth has no cracks, and the skin hidden under them is exactly the skin they
    cover. They follow every body slider.
- **Fabric (data):**
  - `fabric_of` in `tools/sweep_filter.py` cut every composition off after three letters ("100% Cot"). It now
    reads the whole first list of fibres, down to the lining ("60% cotton, 40% polyester").
  - A new `weekly_refresh.py fabric` re-reads every pick from the downloaded catalogues and rewrites the card
    notes. A cut-off value is completed only when its fibre is unambiguous, otherwise it is dropped.
  - Result: 3,057 picks with a full composition (2,946 read fresh from their listings). 1,375 are 100% cotton,
    and the Workwear "100% cotton only" filter now finds them (it found 42 before).
  - `tools/test_fabric.py` checks the reader.
- **Still to do:**
  - The 3D checks over all 574 outfits. A full run was started on the build before these changes and had not
    finished.
  - The gap under the crotch on some trousers and shorts, and the small collar glitches at the side of the neck.
  - Phase 2 (draped garment library, cloth settling, fabrics) as set out in section 4 and in Emma's review doc.

## 2zw. 3D check failures fixed; boots, ties and denim; 2D Dave from Edit Dave; fabric search (7 Oct 2026)

- **The full 3D check (574 outfits) and what it found:**
  - 93 outfits were flagged.
  - Holes: 64 outfits with small holes at the back, nearly all gaps of background between his arm and his side.
    The checker now tells an arm from a body (a top is one piece, so it reads each piece's own arm mask), and
    counts only holes in the clothes.
  - The crotch: a real opening under the crotch, between the seat and the legs. A gusset now fills it, in the
    cloth's shadow colour so it reads as the inside of the crease.
  - Show-through:
    - A hoodie's hood under an open overshirt poked through its back. The hood now lies out over every layer worn
      over the hoodie (it works out how far out each later layer will sit).
    - A tucked-in shirt let the trouser waistband show through. When a shirt is tucked, the waistband and seat now
      stand out by its thickness.
  - Colour: 24 flags, mostly near-white shirts marked "lost its colour". By HSL saturation an off-white counts as
    strongly coloured; the checker now judges colourfulness by chroma, and allows very dark cloth to read a little
    lighter under the studio light.
  - Re-checked: all the flagged outfits pass.
- **Seams welded:** the body has duplicate vertices along its region seams. Tops and trousers built from it now use
  one vertex per position, with averaged normals.
- **Boots read as boots:**
  - Over boots the trouser hem stops higher and stands clear of the shaft, so the toe, laces and start of the
    shaft show.
  - Laces criss-cross up the front of the shaft between metal hooks, with a padded collar. Chelsea and dealer
    boots get elastic side gussets instead.
- **Ties:**
  - A tie is one ribbon lying on the shirt, from a knot under the collar to a pointed blade (narrower when slim or
    knitted). The shirt's buttons are not drawn under it.
  - A bow tie is a bow at the collar.
  - A tie bar or clip is a bar across the tie, not a necklace.
- **Denim colour:** studio shadows and model shots made denim read too dark, or as stripes. Denim now stays within
  its wash: raw, dark and indigo; mid; or light and stonewash. It takes no stripes or checks from the photo
  unless the listing names them.
- **Photo fronts:** a flat-lay photo with its sleeves laid down over the body is no longer laid over his chest
  (cuffs showed on it). A long sleeve edge down the sides of a plain long-sleeved top rules it out.
- **Pattern words:**
  - "Button-down" no longer reads as down-filled: no quilting, nylon shine or down-wash care.
  - Cordura, drawcords and records are no longer corduroy.
  - A gilet is quilted only when the listing says so; duck, canvas and fleece gilets are plain.
- **2D Dave follows Edit Dave:**
  - The drawing takes his skin, hair and moustache colour from Edit Dave.
  - His moustache style (chevron, walrus, handlebar or pencil) and beard (stubble or short beard) match.
  - His eye colour, his brow weight and arch, and his glasses (round or square) match too.
  - Saving Edit Dave redraws the 2D figures as well.
  - The drawing board's background is back (it was lost when the figure became a button), in light and dark mode.
- **2D trousers by cut:** wide legs flare to the hem, barrel legs bow out at the knee, cuffed joggers taper to a
  cuff, and relaxed and regular pairs hang straight. The cut comes from the pick's fit label and name, as in 3D.
  Jeans, joggers and cargos lose the pressed crease.
- **Shop:**
  - A Fabric filter: 100% cotton, natural fibres only, or no polyester or stretch. It is read from each listing's
    fibre composition.
  - Search matches whole words for short words and word starts for longer ones ("red" no longer finds Fred Perry
    or "reduced"). It knows a few synonyms (jeans and denim; cord, cords, corduroy and needlecord), and fabric and
    fit are searchable.
  - "Price drop" needs at least 5% or £1, so a drop of a few pence is not promoted.
- **Sunglasses by shape:** wrap (one curved shield), aviator (teardrops in a thin metal rim), round or square, from
  the listing name, with the frame and lens colours it names (gold, silver, tortoiseshell; amber, green, blue,
  mirrored).
- **Weekly routine:** now runs `weekly_refresh.py fabric` and the 3D checks, and reports their result.
- **Collar leaf:** the folded leaf of shirt and polo collars had a toothed edge over the shoulders. The cloth under it
  is measured from a coarse map, and neighbouring points jumped in and out. Each fold row is now smoothed round
  the neck (a median, then a mean), keeping it just clear of the cloth.
- **Still to do:** one small notch at the back of some polo collars, and then Phase 2.

## 2zx. Full 3D check clean; checks woven from the photo; folded shirts; why each pick suits him (7 Oct 2026)

- **The full 3D check after 2zw:** 3 of 574 outfits flagged (down from 93), no colour faults and no page errors.
  All three were real, and are fixed:
  - **An overshirt over a formal shirt** was tucked in with it, so the trouser waistband (wider for the tucked
    shirt) showed through its back hem. Only the shirt next to him goes in now; an overshirt worn over another
    shirt hangs loose over the waistband.
  - **A gilet over a jumper:** the jumper showed through two patches at the front of the gilet's armholes. That part
    of the gilet is the arm's part of the body mesh, which a top lies closer to; for a gilet it is the body of the
    gilet, so above the armhole it now keeps the gilet's full thickness.
  - **A bag strap** stood off his upper chest (a gap showed from the side). It now follows the outside of what he
    wears, from the top of his shoulder across his chest to the bag.
  - All 76 outfits with a gilet, waistcoat, vest, bag or two shirts were re-checked: none flagged.
- **Checks woven from the photo:** a check's cloth used to be a square cut from the shop photo and mirrored into a
  tile. Cut from a model shot or a folded shirt, it carried folds, buttons, a tee under an open shirt or a size
  badge's lettering, and repeated them as blobs and rows of text. A check is now rebuilt as a weave: each point is
  half the colour of the thread across and half the thread down. Those colours are read from the photo's rows and
  columns; a band that does not vary along its length is dropped. Flannels, ginghams, tartans and Prince of Wales
  checks come out crisp, in their own colours, and repeat cleanly.
- **Prints repeat as they are:** a print's square of photo used to be mirrored into a 2 x 2 tile, which turned a
  floral or a geometric print into a kaleidoscope. The square now repeats as it is, its edges faded into a copy of
  itself shifted by half, so there is no seam and no mirror symmetry. A shirt the listing calls striped, but whose
  photo read as a print (a close-up of the collar sets the stripes at a slant), has its stripes' direction found
  and laid upright.
- **Checked against the last build:** every outfit piece's photo reading (1,370) was compared before and after.
  Colours, patterns and photo fronts are unchanged; only the cloth squares of checks and prints differ.
- **Known limit, skin in model photos:** skin is found by colour, and only lighter skin is caught. A wider rule
  that caught deeper skin tones also caught cream, stone, tan and khaki cloth (a tool belt read as black, khaki
  joggers as grey, several flat-lay tees lost their photo front), so it was not kept. A shop photo of a
  darker-skinned model can still be taken as a flat-lay: one Ted Baker shirt shows the model's hand and trousers
  on its front. The fix needs a check by shape (a head at the top middle, hands at the sides), not by colour.
- **No lettering in fabric tiles:** the square of photo used for a print or check is the one with least "ink":
  pixels far from both of the cloth's colours, such as a size badge, label or lettering.
- **Folded shop photos:** Savile Row Company and T.M. Lewin photograph formal shirts folded in the packet (collar up,
  a cuff across, a square of the cloth in a corner) or as close-ups of the collar. These photos are no longer laid
  over his chest as the shirt's front, which drew a collar and cuff on it.
- **This week list:** each new pick now has a line saying why it suits him: the fit he likes (relaxed or wide
  legs, which don't grip), 100% cotton or natural fibres, extra-wide fittings, his size in stock, and how much is
  off.

## 2zy. Workwear kit, belts, lighter card renders, cleaner photo fronts (7 Oct 2026)

- **Synced with the other session's work (PR #12):** the contributor guide, the pull-request 3D check on five body
  builds, `data/fixes.json` corrections, pocket squares, navy kept navy, and tucked shirts kept inside the trousers.
  The claude.ai artifact was republished from `main` (version 32), and the GitHub Pages copy was confirmed to match it
  byte for byte.
- **Workwear kit is worn over the clothes.** 24 Workwear outfits have tool belts, clip-on holster or nail pockets,
  pouches, hammer holders or a half apron. They were drawn as a thin belt that any untucked top hid. Now:
  - a tool belt goes round his hips over the top, with a buckle and a pouch each side;
  - clip-on pockets hang from the waistband (just under a top worn over it) at the front of each hip, leaning in to
    lie on the thigh and narrowing to the bottom;
  - a hammer holder has its steel ring, and a half apron hangs in front with two pockets.
  All are placed outside what he wears there, read from the maps of his clothes, so they fit any build.
- **Belts show.** With a trouser belt, a shirt or polo is tucked in (never with shorts), in 3D and in the 2D drawing.
  The belt goes round the waistband with its loops over it and a buckle at the front, and in 2D it is drawn on the
  waistband under anything worn open on top.
- **Lighter hair on the outfit cards.** Dave's curls were about 1.9 million of the 2.0 million triangles in each
  card render. Cards now use two hairs a lock on a coarser spiral, which looks the same at card size: about 0.45
  million triangles a card. The 3D view and the 3D check keep the full hair.
- **Cleaner photo fronts.** On a flat-lay the background between a sleeve and the body is closed off, so it was laid
  on his sides as pale slivers. It is now cleared from the front's sides inward once the front has passed its checks.
  Every outfit piece's reading (1,369) was compared with `main` before and after: none changed.
- **One correction** in `data/fixes.json`: Samuel Windsor's open-collar knitted polo, a navy flat-lay on a grey
  gradient, read with a grey panel and lilac sleeves. A corrected colour now also drops the photo's sleeve colour.
- **Sets worn as two pieces:** a correction can now hold `shapes`, corrections for one garment shape only, so a set
  sold as one listing (Tokyo Laundry's Keir tee and shorts, one photo) draws a black tee and grey marl shorts. The
  build checks them like the rest.
- **Trousers:** the press that closes the legs at the inner thigh was measured in steps of height and jumped from one
  ring of the leg to the next, leaving thin creases across the inner thighs on most trousers. It is now evened out
  over the cloth (never less than it needs, so no light shows between the legs).
- **Tucking, one rule for 3D and 2D (`tuckList`):** a shirt worn open hangs loose. In `rv-black-smart` an open shirt
  was tucked in over a vest left hanging out, and the vest came through it (poke 167, also on `main`). A tee or vest
  under a tucked shirt now goes in with it.
- **Sunglasses:** the arms run back along the side of his head to the ears, measured on his head slice by slice; they
  used to go straight out to the ears' width and stood off his temples.
- **Checks:**
  - All 55 belted outfits pass the 3D check on his saved build and on the slim, athletic and heavier builds. On the
    loose fit the one flag, `wk-chore`'s collar, is the same on `main`.
  - Full run, all 574 outfits on his saved build: one flag (`rv-black-smart`, above), now fixed.
  - The 31 outfits touched after that run (sunglasses, the Keir set, open shirts with a tuck) pass.
  - The pull-request check (gate set on five builds) passes.

## 2zz. Visual survey fixes: outer layers, cargo pockets, model photos by shape (7 Oct 2026)

A survey of 16 random outfits beside their shop photos found these, now fixed:

- **An overcoat under the suit jacket** (`winter-formal`): outer layers had no order among themselves, so the suit
  jacket was built outside the overcoat and only the coat's skirt showed below it. Outer layers now go on in wearing
  order (blazer, gilet, jacket, coat or gown), in 3D and 2D.
- **The overcoat's colour:** "Blue Navy" read as mid blue from its first word. It is corrected in `data/fixes.json`;
  two-word colourways mix both orders ("navy blue", "olive green", "charcoal grey"), so the reader was not changed.
- **Blazer pocket flaps** sat at the depth of the body's middle and stood proud of the blazer at the sides, pushing
  bumps into a coat worn over it. They now lie on the blazer where they are.
- **Cargo pockets** were thin slabs standing out from the thigh like fins. They are now a patch round the outside of
  the thigh, filled out a little in the middle and flush at its edges, with a darker flap across the top and a
  stitched edge.
- **Model photos found by shape:** a shop photo of a model has a head above a narrower neck above the shoulders,
  whatever his skin colour; a flat-lay widens from the collar straight to the shoulders. Its front is no longer laid
  over Dave's chest. Compared over every outfit piece: four model-photo tees (stone, sand, orange and yellow, where the
  colour-based skin test had to stand down) lost their fronts, and nothing else changed. A Ted Baker shirt on a
  darker-skinned model, whose hand and trousers used to show on the chest, is now read as a model photo too. Hoodies
  are left out (a hood up on a mannequin is the same shape).
- **A pale yellow sweatshirt** laid flat with its sleeves over the body put the sleeves' outlines on his chest; its
  front is turned off in `data/fixes.json`.
- **Stripes the photo could not measure:** a shirt whose listing names stripes, but whose photo is a slanted close-up
  of the collar, a folded shirt or a model in shot, was read as a print: a blurred, mirrored square of the photo, on
  one shirt tinted by the model's skin. Such shirts are now drawn as clean upright stripes. The ground is the cloth's
  main colour and the stripe the colour of the darkest tenth of its threads, kept a deeper shade of the cloth when
  those threads are skin or grey. The stripes are fine on most shirts and broad for a random, bold, block or awning
  stripe. Seven outfit shirts changed, each checked beside its photo (Charles Tyrwhitt poplin and Oxford, Brakeburn,
  Uniqlo, M&S, Savile Row's random stripe).
- **Close-up photos** (the frame filled with cloth, almost no background) now scale their stripes and checks to about a
  quarter, since they were measured against a garment far longer than what is in frame. Three outfit pieces are
  close-ups today, all plain, so nothing visible changed yet.
- **Brakeburn's Shirwell resort shirt**, photographed by the sea, read grey from the sky and water; it is corrected in
  `data/fixes.json` to mid blue with thin white stripes.
- **Checks:** the full 3D check over all 574 outfits on his saved build flagged none (no skin, holes, pokes, stray parts
  or colour drift, no page errors), and the pull-request check passed on all five builds.
- **Looked at and right as drawn:** a striped bomber (it is striped), a dark teal "black" gilet (the photo is teal),
  two-tone half-zips, and day-pack straps over a waterproof.

## 2zzz. Open footwear, overshirts over knits, argyle (7 Oct 2026)

A third survey of 16 random outfits, in 3D and in the 2D drawing, found these, now fixed:

- **Sliders, sandals and flip-flops were closed shoes** (in 3D a shoe shape, in 2D laced shoes). They are now open:
  his own bare foot stands on a footbed, held by a slider's wide band, a sandal's straps across the toes and instep and
  round the heel, or a flip-flop's thin Y. The straps and footbed are fitted to his foot's outline, measured on the
  body slice by slice, so they fit any build; in 2D the foot shows bare under the straps. 19 outfits; all pass the 3D
  check on his saved, slim and heavier builds. `h10-resort` joins the pull-request gate set.
- **A chore jacket under a knit** (`wk-chore`): every overshirt was drawn under knits, so a chore jacket's collar came
  through a jumper's neckband on the loose fit. A jacket-weight overshirt (chore jacket, shacket, nylon, canvas,
  insulated, borg-lined) now goes over a jumper or hoodie, worn open; flannels and light overshirts stay under, collar
  out. 3D and 2D share one layer order (`layRank`).
- **Collar bands dipping into the collar below:** each point of a knit's neckband was pushed out on its own to stand
  on the collar under it, so the band followed that collar's outline and showed it through teeth on the loose fit. The
  rows are now evened out round the neck. On the loose fit, three of four collar-under-knit flags cleared; the fourth
  (`ramsey-street`, poke 31 against a limit of 30, a collar peeking out of a hood) is noted in the handover.
- **Argyle** was a square of the model photo: folds, an arm, smears. It is now drawn as argyle, diamonds in the
  cloth's two colours (the second taken from the whole garment, not the square) with thin crossing lines, in 3D and 2D.
- **Model photos give no chest print:** a graphic tee photographed from behind on a model put his hand and the back
  print on Dave's chest. One item changed.
- **2D: open short-sleeved shirts** were drawn with full-length sleeves; they keep short sleeves now.
- **Corduroy trim** ("with corduroy trim", "cord collar") no longer makes the whole garment corduroy (a quilted jacket
  showed pinstripes in 2D).
- **A jacquard scarf** listed as "Lilac" is a deep navy-purple in its photo; corrected in `data/fixes.json`.
- **Checks:** the first push turned the pull-request check red. The new strap code declared its own `band`, which
  shadowed the shared helper, so boots and socks failed to build. It is fixed, and the lesson is in the guide. On the
  final build, the full 3D check over all 574 outfits flagged none, with no errors, and the pull-request check passed on
  all five builds.

## 2zzzz. Prints, cloth over the shoulders, gilet shoulders, trainer soles (7 Oct 2026)

A fourth survey, of more outfits in 3D and 2D and of every trainer, shoe and boot beside its photo, found these, now
fixed:

- **Shorts worn as trousers:** the three Ted Baker Halbak listings are chino shorts. Three outfits now draw them as
  shorts, and three that wanted trousers wear full-length chinos or cords instead (names and price notes follow).
- **An all-over geo print read as a tartan:** a print that repeats both ways looked like a check to the photo reader.
  When the listing names a print that is not a grid (all-over, AOP, geo, floral, paisley, camo, spots) and no check, it
  is now drawn from a square of the photo itself. Two Lambretta tees changed; no other reading moved.
- **Prints and stripes smeared over the shoulders:** the cloth's texture ran up the body by height, and across the
  nearly flat tops of the shoulders the height hardly changes, so a print or stripe was pulled into streaks there and
  on the sleeve head. It now runs by length along the cloth, over the shoulders and up each sleeve, and round each
  sleeve row by that row's own length. Stripes and checks now carry on evenly over the shoulder.
- **A jumper through a gilet** (`g-quiet-26`, loose fit, also on `main`): the front of a gilet's shoulder lies on the
  arm's part of the body mesh, and those points only cleared his arm, not the shoulders of the jumper under them. They
  now clear both. All 46 gilet and vest outfits pass the 3D check on all five builds.
- **Trainer soles were always white** and their side stripes white or black. The photo reader now finds a trainer's
  sole (the commonest colour at the bottom of its outline, column by column, in product shots only; a tan gum sole was
  being taken for skin) and a bright accent too small to be a second colour. A black hiking sole, a gum cupsole and red
  stripes on blue now show in 3D and 2D. Shoes and boots keep their dark (or named crepe, gum or wedge) soles: their
  photos' floors and reflections read as soles.
- **Pale garments on pale backdrops:** M&S ecru pleated cords (the backdrop took the trousers, and one outfit called
  them brown) and the Farah Netherton ecru shirt (its photo's middle is the tee under it) are corrected in
  `data/fixes.json`, with the adidas VL Court (white with green stripes), the Columbia Konos Trillium (not its pale
  midsole) and Grafters brogue Chelsea boots (tan, not their elastic sides). Two summer outfits wore M&S Oxfords as
  "grey": the photo is the brown colourway.
- **Checked and left as they are:** the dark olive and fudge cords read as their photos (dark photos, not a reader
  fault); a corduroy-specific colour rule moved nothing and was dropped.
- **QA tools:** `multi.js` takes a view (`chest`, `legs` or `feet`, the feet turned to show the shoe's side as shop
  photos do) and waits for the photo reading; `dump.js` reports footwear soles and accents.
- **Checks:** on the final build, the full 3D check over all 574 outfits flagged none, with no errors; the pull-request
  gate set passed on all five builds, as did every gilet and vest outfit and the 26 footwear outfits touched.

## 2zzzzz. Emma's comments on the 3D model, and why they happened (7 Oct 2026)

Emma left ten comments on the artifact about pieces that did not look like the real thing. Each was traced to its
cause, and the cause fixed for every item it affects, not only the one commented on.

| Comment | Cause | Fix (for every item it affects) |
| --- | --- | --- |
| Ringer tee "merging the listing background" | Its photo is padded with black bars and smeared edge pixels, laid on the tee as its front; ringers had no trims | `fixes.json`: no photo front; ringers draw their contrast neck and cuff bands (3 tees) |
| Shorts blue, listing beige | A name with no colour fell back to the outfit's own colour word ("navy"), which won over the photo | The outfit's word only stands in for legwear on a model shot; the colourway in the shop's link (M&S `?color=`, Uniqlo colour codes) is used; trouser photos on models read the legs, not his top (93 readings corrected, all checked against their photos) |
| Resort shirt pattern wrong | A lifestyle photo with no close-up; the name does not say striped | `fixes.json` takes a cloth swatch (`swatch`), cut from the shop's close-up product image |
| Shirt wrinkled, not fitted | A crumpled flat-lay photo laid on as the shirt's front | Plain woven shirts no longer use a photo front (15 shirts); every other photo front has its creases softened |
| Shoulder "hem" not normal | Each neckband pushed out to the body's surface, which at the sides is the slope of the shoulder: a flat tab over each shoulder | Neckbands and collars measure only his neck there |
| Crotch looks like a hole | The body dips back between the legs at the front and the trousers followed it into a narrow slot; a dark filler showed through it | The cloth is brought level across, and a panel of the trouser's own cloth closes the slot behind it (all trousers and shorts) |
| Hoodie hem and hood | A crew rib neckband and a flat triangle on the back | A hood worn down: a rim standing round his neck, low at the front where its edges meet and higher behind, turned over at the top, with the hood lying on his back below it |
| Rain mac like leather | Nylon was almost as glossy as leather; rain jackets had no hood unless the name said "hood" | Nylon is matte with a fine crinkle; rain jackets, cagoules and "waterproof jacket"s have their hood |
| Hat wrong, not on the head or hair | A fixed-size dome floating above any head; ten baseball caps listed as flat caps | Caps are made on his head (from the skull map), with the band from brows to nape, a baseball cap's six panels, button and curved peak, a flat cap's low crown carried forward; curls show below the band; the build now checks a hat's shape against its name (13 corrected) |
| Clip-on holsters not like the images | A plain box with a flap | Holster pockets drawn as sold: open-topped, two layered pockets with slanted taped tops, belt straps; the pair mirror each other |

Further faults found while fixing these, fixed the same way:

- **Waffle cloth** drew as vertical ribs; it is now a small grid (47 items). **Self and tonal stripes** ("self stripe")
  drew as contrast stripes; they read plain.
- **Shirt buttons** were white on every shirt; they are tonal (a shade of the cloth, pearl on white) and sit on the cloth.
- **Knit hem bands** showed broken, patchy ribs where a photo front ran over them; photo fronts now stop at the band.
- **Two hats** listed as baseball caps are a watch cap and a swimming cap; they draw as beanies.
- **Named neutral colours** (black, grey, charcoal) agreed with strongly coloured photos by distance alone (a red
  check shirt "dark grey"); a neutral name now wants a neutral photo.
- **QA:** `inject.py` exposes `descOf` and `byId`; `dump.js` reports the photo's colour when the name's wins (`c1p`).
- **Coat necklines on a jumper:** on the athletic body a coat's neckline met a jumper's neckband (cold-commute,
  back poke 40). The coat now clears the neckband measured a little above, below and either side of the neck point.
- **Checks:** CI (60 changed outfits plus the gate list, on all five bodies) flagged only that neckline. Rerun on
  this build, the three jobs that flagged it come back with 0 flagged.
  The full 574-outfit run was stopped part-way to ship this. The weekly routine runs it in full.

## 2zzzzzz. Page features from the plan, one dress code, a wear log, stored specs, hats on his head (8 Oct 2026)

Pull request #18. Everything here needed no decision from Emma; the Three.js upgrade and Blender templates were not
started.

**Page**
- **Back button and links to an outfit.** Moving between views is a step in the browser's history, so Back and
  Forward work; `#fit/<id>` opens one outfit large (Back closes it), and "Copy a link to this outfit" shares it from
  GitHub Pages. The root page's redirect keeps the address.
- **Shop by budget.** £60, £100 and £150 buttons (Outfits and Build) suggest a whole outfit from photographed picks
  in his size and open it as a flat lay of the shop photos, to scale.
- **One dress code.** A formality scale from 0 (lounge) to 4 (tailored), defined once (`FORMALITY` in
  `tools/build_site.py`) and shipped to the page in `meta.json`. The builder's suggestions and `make_outfits.py` keep
  an outfit's clothes and shoes within 2 of each other (3 for Rave and Lounge), and the build notes outfits outside
  it. 14 of 574 outfits were; 13 generated ones (mostly brogues or derbies with shorts) had the clashing piece
  swapped for a photographed one in his size, and the curated Street "smart" look stays as it is. Python and the page
  give every one of the 7,474 picks the same level. Suggestions also stopped offering slippers outside Lounge,
  joggers outside Lounge and Rave, and slides without shorts (60 sample sets checked).
- **His wardrobe: a wear log.** "Wore it today" on each piece, "He wore this today" on an outfit from his wardrobe;
  each piece shows times worn, the last date and the price per wear, and the list says what he wears most and what
  has not been worn in 30 days.
- **Accessibility.** `lang="en-GB"`, a main landmark and a skip link, the view buttons as a group (not a tab list),
  the large view labelled by its title and focus returned to the button that opened it. axe-core: 0 violations on
  all seven views, light and dark.
- Whole-word search for short words was already in (re-tested: "red" no longer finds Fred Perry or "reduced").
- **Size check per shop.** `tools/size_charts.py` reads each shop's own men's size guide (direct requests and headless
  Chromium only) into `data/sizecharts.json`: what M, L and XL mean there, as the chest it fits (body charts) or the
  garment's own chest, with the collar where the chart gives it and the page it came from. 61 shops so far, covering
  2,486 of the 4,497 tops; 113 are still to read or have no chart. Each top's card says "Size check: L here fits a
  41–43in chest". With his chest on the measuring card it says whether it is in his L there, or which size is
  nearer; without it, shops whose L is for a smaller or larger chest than most (Closure London, Cernucci, Ted Baker,
  howies...) are marked as running small or large.

**Shops**
- 16 picks: BrandAlley (new: Lyle & Scott, GANT, Oliver Sweeney), the M&S sale (Seasalt, GANT, Tommy Hilfiger,
  Timberland, BOSS, Lacoste, Jones Bootmaker) and Berghaus, all checked in his size from the size buttons the pages
  show. A pair of M&S chinos was left out (31in leg only, 25% stretch). Gap, Next, Levi's, Vans, Timberland, Dr
  Martens, New Balance, TK Maxx, Very, Urban Outfitters, Pull&Bear, Bershka and F&F refuse direct requests and
  headless Chromium alike: they need a home computer, as the blocked photos do.

**Phase 1: stored product specs**
- `tools/specs.js` runs the page's own readers over every item worn in an outfit (1,358 pieces, about 20 seconds,
  the same file every run) and writes `data/specs.json`: colours, pattern and spacing, cut, collar, neck, zip,
  pockets, cloth, details and what the photo showed, each colour and pattern with its source and a confidence.
- The pull-request check reads every piece again and fails when that differs from `data/specs.json`
  (`tools/qa/specs_diff.py`), so a change to how pieces are read is committed, and reviewed, with what it moved.
- First labelling pass from it: 23 pieces had a pattern named in the listing that the photo reading drew plain.
  Looked at against their photos, 18 are right as plain (tonal, too fine to see, or on the back only). Five were
  corrected in `data/fixes.json`: the Lambretta Geo AOP and Paisley tees, the Tog24 camo ski jacket and the Service
  Works polka-dot chef trousers take a square of the cloth cut from their shop photo, and the Hawes & Curtis striped
  Oxford (no photo stored) draws its blue and white stripe. 156 pieces where the photo disagreed with the named
  colour (and the name won) were looked at next, on contact sheets against their photos. Most were right (the
  stored photo shows another colourway than the link). The wrong ones had causes in the reader, now fixed for every
  item: a shade word was dropped ("light olive" drew dark olive, "ice blue" mid blue, "dark khaki" pale khaki); a
  denim wash read as a colour ("Stone Wash" shorts and Stan Ray "70's Stone" jeans drew beige); a colourway list was
  read from its last colour ("Black - Asphalt - Platinum Grey" drew grey; "Forest Green - Orange" orange); a model
  name read as a colour (Luke 1977 "Red Rock" boots drew red); "denim" named the cloth, not the colour, in
  "Denim Bucket Overdye Choc"; and olive and khaki had to match one exact shade. 41 pieces now read differently,
  every one checked against its photo; the 64 outfits that use them pass the 3D check.

**3D**
- **Beanies and bucket hats are made on his head,** as caps already were: a snug ribbed crown with its cuff turned up
  and rolled, or a level crown with a flat top and a brim sloping down and out (shorter over his face, so his eyes
  show), each with its lower edge tilting from his brows to the back of his head and the curls showing below it.
  The top of the skull map dips at the crown, which dented the hats; it is smoothed under them.

**Checks:** build clean; smoke test 2D and 3D with no page errors; 3D check (Dave) on the 13 swapped outfits, the 11
outfits with corrected pieces and all 57 hat outfits; CI on all five body types for the changed outfits and the gate
list.

## 2zzzzzzz. Emma's eight comments of 8 October, the rule behind each, and a guard for each (8 Oct 2026)

Each comment was traced to the rule that drew a whole kind wrongly, fixed for every item of that kind, and given an
automatic check so it cannot come back unnoticed (CONTRIBUTING.md, "Lessons learned"). Every check was run on the
build before the fix, where it must flag the fault, and after, where it must pass.

| Comment | Cause | Fix | Guard |
| --- | --- | --- | --- |
| Fair Isle jumper drawn without its pattern | the listing's "camel" (the yoke only) overrode the navy photo, and the reader refused a front that is mostly not camel | `named:false` and `front:true` in `data/fixes.json`; the reader honours both | specs check refuses any `unseen` piece; all 18 were looked at: 9 now drawn with their stripes, checks or prints, 9 confirmed plain (tonal, pin-spot, trim only) |
| Shirt collar over the scarf at the back | the scarf cleared the tops' bodies, not their collars, and only straight back and front; its lower edge sank into the jumper's shoulders | every collar is measured too, in 24 directions round the neck; the lower edge rests on the shoulders; the loop narrows gently going up (the figure is warped to his proportions after it is built, which carried a steeply narrowing neck warmer inside a padded collar) | `under` in `check_3d.js` |
| Gaps in the knit jacket show the shirt as it turns | the tee's photo front had a depth offset that grows at glancing angles, so it came through the jacket as dark streaks (the check's ID pass had no offsets and never saw it); a slit along the open zip tape | a constant small offset for photo fronts and prints; the tape laid over the edges | `offset` in `check_3d.js`; its ID pass keeps each piece's depth settings |
| Sunglasses not the Wellington shape | unknown frame names fell through to a flat box | frames drawn from their named shape (round, oval, Wellington, square, wayfarer, browline, aviator, wrap), acetate or wire, sized to his face; wraps a curved shield with a nose cut-out | `build_site.py` stops on a frame shape the model cannot draw; specs record each pair's frame |
| Jacket and shirt stand out too far | knits hung straight from the chest to the hem | a ribbed hem draws in round his hips; outer layers 5 mm less ease | (look at the side view) |
| Trousers stretched, crotch sticks out | the legs were pressed together down to the shin, and the hip cloth's inner thighs followed his body between the parted legs | the press works only just under the crotch; the legs part below it; the hip cloth follows the legs | `legs` in `check_3d.js` |
| Legs stuck together at the thighs | as above | as above | `legs` |
| A baseball cap, not a flat cap | a tall dome stopping at the band, its peak standing out in front | a low top, highest over the back of his head, carried forward to a lip over a short peak; herringbone cloth | `form` in `check_3d.js` (how far the peak reaches past the crown) |

**Checked for the same faults across the catalogue**
- *Named colour over the photo* (the Fair Isle jumper's cause): all 137 pieces whose listing's colour word won over a
  photo that disagreed (`"src": "name"` in `data/specs.json`) were put on contact sheets beside their photos. 37 were
  wrong and now have entries in `data/fixes.json`: generic words drawn as the wrong shade (a pale sage "green" drawn
  forest green, a sky-blue "blue" polo drawn mid blue, "stone" drawn pale on tan and shale cloth), caps and a tee whose
  named colour is only the peak or the sleeves (`named: false`; a new `slv` field gives raglan sleeves their own
  colour), and four patterns drawn plain (stripes, a patchwork print, knitted chains). The other 100 are right: mostly
  shop photos of another colourway than the one linked, where the named colour is the one he would buy.
- *Patterns named but drawn plain*: all 18 `unseen` pieces (see the table above).
- *A pick filed as the wrong kind of clothing*: a denim bucket hat was filed under trousers and worn as the trousers
  of two outfits. It is now an accessory, the two outfits wear dark jeans, and `build_site.py` stops on a hat drawn as
  anything else and notes any hat filed under another kind.
- *Picks that are not his*: 37 women's picks had come in by routes other than the shop sweeps (whose filter already
  refuses them): 30 Jack Wolfskin "W" lines, "Women" in Sergio Tacchini and Fila titles, River Island cinch-back
  pieces, an adidas "Japan W". Removed; `build_site.py` now stops on a women's listing.
- *Size check on things that are not tops*: socks, boxers, slippers and shorts share categories with tops and were
  given a chest chart's line; it now shows on upper-body garments only (2,585 picks). 20 more shops' charts were read
  (81 in all).
- *Sunglasses*: all seven pairs drawn in their named frame; one with no shape word (A.Kjaerbede Noah) is now described
  as slim rectangular silver with pale blue lenses, as its photo shows.

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
2. ~~**Photo strip on outfit cards.**~~ Done: the card's board shows the listing photos whenever a piece has one.
3. ~~**Price-drop watch on the shortlist.**~~ Done in round two.
4. ~~**"Shop by budget" quick sets.**~~ Done in 2zzzzzz.
5. ~~**Shop filter in Picks.**~~ Done in round two.

### Step 4b: Features suggested for next round
1. ~~**Shop-by-budget sets.**~~ Done in 2zzzzzz.
2. **Price-drop alerts on the shortlist:** re-run `shopify_pull.py` weekly for the shops behind
   saved picks and set `prev` and `hist`, so the shortlist's "Down £x since it was saved" lights up.
3. ~~**Size check per shop.**~~ Done in 2zzzzzz for 61 shops; `tools/size_charts.py` adds more.
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

### Status after the 6 October 3D update (pull request 7)

That update landed during the review: a real CC0 human body with the Edit Dave editor, listings read for
collar, neckline, zips, pockets, fit and material (`descOf`), photos read for stripes, checks and chest prints
(`readLook`), the shop photo's front laid over flat-lay tops, trouser cuts from the listing, zip up or
unzip, flat hoods, and listing colours winning over bad photo reads. Re-rendering the same 12 outfits on
it (main at 517a37e):
- **Now right:** brown trainers, a closed hip-length Harrington, the tie, no skin gap under hoodies, and a
  natural body.
- **Still wrong:**
  - Denim jacket sky blue; stone trousers near white; tan trainers pale yellow.
  - Every boot still a low shoe.
  - Gilets still forced to quilt (`texOf`, `sh==="gilet"` gives "diamond").
  - "button-down" still matches `down` in `texOf`, the loft rule, the material rule and the care text.
  - Oxford weave read as stripes.
  - Belts hidden under untucked tops; no rib bands or cord collars on blousons; sunglasses one shape;
    one wrong photo (the Timberland boots).

So phases 1, 2, 4 and 5 below are partly done. The work that remains is the core: specs stored once
per item rather than read on every visit, draped templates per archetype, shoe lasts and boots, a fabric
library, ease-driven layering, and the weekly check. The line numbers in the rest of this section are
for commit 9e3f504, before that update.

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
