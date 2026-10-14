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

## 2zzzzzzzz. Emma's three comments of 10 October, and faults found on the way (10 Oct 2026)

The artifact had not been republished since 7 October, so the fixes in pull requests 18 and 19 were not live when
Emma commented; version 38 published them first. The three comments still showed on that build:

| Comment | Cause | Fix |
| --- | --- | --- |
| Fair Isle half-zip: "still no design like the listed half zip" | the photo's front was laid on as a flat patch on the chest, so the camel yoke, the band across the sleeves and the hem showed nowhere else | a new correction field, `place`: the jumper's front panel cut from the listing photo (centre to side seam, collar to hem), laid on every part of the piece by height, mirrored round the body and run round each arm, in 3D and in the 2D drawing |
| "Thighs still sticking together" | the legs only parted 14 cm below the crotch and by 2 cm, and each leg followed his knee and calf, so they read as one block | each leg hangs in straight lines from the thigh over the calf to the hem; the gap opens as a V straight from the crotch |
| Summer weekend: "shape doesn't match" | deck shoes were drawn as dress shoes, the Wellington frames as squares, and polo and shirt collars stood up like a band | deck shoes get a flat rubber sole in the photo's colour, a moccasin apron with pale stitching and a rawhide lace round the collar tied at the front; Wellington frames are a soft trapezoid; collars are low at the front and high at the back, and their fold spreads out over his shoulders and chest |

Found while fixing these, and fixed for every outfit:
- **Normals thrown away after building.** The figure is warped to his proportions after it is built, and that step
  recomputed every surface's normals, losing every adjustment made to them (the cloth over the hips turned to meet the
  legs, tube seams, the body's welded seams). They are now kept and turned with the warp.
- **A ring round both thighs** where the cloth over the hips met the legs: the leg tops tucked in under it, leaving a
  lip that showed the inside of the cloth; the cord's wales also stepped sideways there. The leg tops now run on under
  it at almost the same size, and the texture is mapped by the same angle on both.
- **Corduroy drew as 2.5 cm awning stripes.** Wales are now about 3 mm apart, with a lit crest.
- **A dark block on the inner thigh** with a hard edge at 0.6 m (the contact shading doubled there); it now eases in.
- **Saw-tooth skin at every shoe's opening**: his foot was taken away whole, though it reaches above the opening at the
  ankle bones; now only the part wholly inside the shoe goes.
- **Flat-faced toes** on every shoe: the toe is rounded off.
- **QA:** `tools/qa/card.js` draws the outfit cards exactly as the page does (the light build, soft shadows, turned
  0.32), beside a 3x crop, since the comments are made on the cards.
- **Checks:** the gate outfits and the three commented ones on dave, heavier and loose; CI runs the same on the pull
  request.

Still open (for the review and plan Emma asked for next): the polo's belt hides under its hem with shorts and its
keeper shows through (tops are tucked for a belt only with trousers, in 2D and 3D alike); grey shards where a folded
collar's ends meet the shoulders; small specks on the Harrington; the 2D drawing reads the Brakeburn cords' wales as
brown stripes rather than rust cord.

## 2zzzzzzzzz. The fitting room upgrade, from the Claude Design proposal (10 Oct 2026)

Emma asked for the "3D Fitting Room Upgrade" design to be built: one fitting room with three modes, the model taking
most of the screen, pieces pinned to him, and Edit Dave cut down to the essentials.

- **Outfit view** (the large view, `openZoom`, `FR`, `frShell`/`frFill`): the stripe, a header with the outfit's place
  in the list, total and saving, and 3D model / Photos to scale / Split / Drawing. Pieces sit down the left, outermost
  first, and are numbered as the **pins on him**. Each pin is put by rays on the front of the piece, so it never sits
  on something covered (`anchor` in `Live3D`). Pins follow him as he turns and fade when the piece faces away.
  - **How it's worn:** jacket open or done up, top tucked or untucked, trouser hems with a break or turned up. These
    are global overrides (`ZIPM`, `TUCKM`, `TURNM`), read by the same rules as the as-worn look (`tuckOn`, `turnOn`,
    `tuckList`) in 2D and 3D.
  - **Light:** Studio (what the checks see), Daylight or Evening (`LIGHTM`, in `make3Dcore`).
  - **Camera dock** (Front, ¾, Side, Back; Full, Top, Feet, Face; Turn), a **turn bar** and a height ruler.
  - **Chosen piece:** its photo, price, Buy, Shortlist and Hide on him. "Try instead" swaps from `swapOpts` and shows
    each on him while it is hovered.
  - **Outfit strip:** still renders of the outfits round this one. ← and → (or a swipe on a phone) flip outfits and
    keep the camera and light.
- **Edit Dave** (`CES`, `ceForm`, `ceSlider`, `ceFrame`): sections down the left with a count of unsaved changes per
  section. Body type cards with a figure each. Six sliders up front (height, weight, muscle, shoulders, waist, leg
  length) with the average man (|) and his saved setting (◆) marked; the rest sit under Fine-tune. Measuring lines on
  the model and a measurements card checked against the sizes he buys. **Compare with saved** shows a still of the
  saved Dave from the same camera, wiped against the live one (`Live3D.still`). The header counts unsaved changes.
- **Compare** (`CMP`, `cmpRender`): up to four outfits side by side, from Compare on any outfit card or in the
  fitting room. Still renders at the chosen angle (`snap3D` takes a rotation and can jump the queue), one column live
  at a time, Turn steps them all round together, and a weather line.
- **On a phone:** the model on top and a sheet below (Pieces, Swap, Dave) with a full-width Save; Edit Dave has
  Cancel / Save, sections as chips and larger sliders.
- **Checks:** the as-worn 3D builds are unchanged (studio light, no overrides). The gate set passes as worn, with
  `--wear tuck=in,turn=up` and with `--wear zip=up,tuck=out` (new options in `check_3d.js`).

Known and left for later:
- **A done-up blazer** (buttoned at the waist, shirt and tie in the V) is not drawn: the old Zip up button closed it to
  the neck with the tie over it, and the new CI wear check caught it (collar poke on `wedding-guest`). Blazers now stay
  as worn under Open / Done up (`zipBy`) until that front is built. A shirt worn with a tie also always stays tucked in
  (`tuckOn`), so Untucked is not offered with a tie.
- A coat done up kept its open-front collar gap, so the shirt collar showed at the sides of his neck (`cold-commute`,
  poke 39). Its collar now comes further round when it is closed (gap 1.0 instead of 1.7); coats are open as worn, so
  no as-worn build changes.
- The model's measurements (chest about 34in on his saved shape) say S/M tops while he buys L. The card says so
  plainly; either the measurement or his saved shape needs a look with Emma.
- `swapOpts` offers some odd swaps (a denim hat for jeans): `derive` reads "Denim … Hat" as trousers.
- The Fitting room fold under Style guide and the builder's small model still have their own controls.

## 2zzzzzzzzzz. Swaps by name, a blazer done up (11 Oct 2026)

`STATUS.md` is new: the working file with what is in progress, the queue and a log of what shipped. Keep it current.

- **Swaps (PR #23):** the fitting room offered a denim hat as a swap for jeans. `guessShape` went by the shop's
  category first; it now reads hats, caps, socks and gloves by their name. The build already warned about a hat filed
  under another category, but `is_hat` gave up on any name with an accessory noun, so it never fired; fixed, and it is
  now an error. Four hats were refiled. `sweep_filter.category` knows a plain hat and files socks as basics.
- **A blazer done up (PR #24):** buttoned at his natural waist (`BL.crotch + 0.22`), the shirt and tie in a V up to
  the collar, the lapels running down to the button, the fronts curving apart below it and his left front lying over
  his right. In 3D the fitted body takes an opening that changes with height (`gapAt`, each row's columns spread over
  the cloth that row has); in 2D the panels meet at the button. The Open / Done up toggle now works on blazers
  (`zipBy`). All 14 blazer outfits pass the 3D check done up and as worn.
- **Shirt collar and tie (PR #25):** the tie's heights were the drawn figure's, so on the real body its knot hung 6 cm
  under the collar, on his chest; and it was laid on the outermost layer, so it came out over a blazer done up. It now
  lies on the shirt itself (rays at the shirt's own meshes and placket), with a four-in-hand knot at his throat filling
  the collar's notch. The collar's leaf comes further down at the front and its two front edges angle apart to the
  points (`fold.spread`), where they used to drop straight from the stand's notch. The gate set and all nine tie
  outfits pass the 3D check as worn and done up. Left: the blazer collar is ragged at the sides of his neck.
- **Shoe lasts (PR #26):** every shoe was the same long, even pod on a grey slab. A last is now chosen from the name
  (dress, Chelsea, loafer, work and safety, hiking, boot, desert and chukka, skate, trainer) and scales the profile
  slice by slice: slim almond toes, a low loafer vamp, a bulbous safety toe cap, a round desert toe. Soles by kind: a thin
  dark sole with a stacked heel, a thick lugged sole, a pale crepe sole. Boot shafts by kind (a Chelsea to just over the
  ankle, a desert boot to the ankle). Loafers get their apron seam and a penny strap or tassels. The upper has its own
  geometry, flat on the sole with a rounded toe. A spread of 55 outfits covering every kind passes the 3D check
  (one flag, `od-event`, is on main too and has nothing to do with shoes; queued in STATUS.md).

## 2zzzzzzzzzzz. Trousers cut as a pair: why the legs kept sticking together (12 Oct 2026)

Emma: "the legs are still getting stuck together and the crotch is still a bit of a mess ... work out why we keep
running into this misshaping on the renders and ensure it stops."

- **Measured on main:** rays across between his legs found the two trouser legs overlapping each other (by 5 mm, and up
  to 7 cm at the front of the crotch) from 6 to 18 cm below his crotch, while his own thighs are 19 to 31 mm apart
  there. They only parted 18 cm down.
- **Why it kept coming back:**
  - The trousers' top (`lowerWrap`) was his own skin over the hips and the tops of the thighs, pushed outward by the
    ease. Where two parts of him nearly touch, that fails: the inner thighs, each pushed toward the other, met and
    crossed in the middle, and the cloth traced the bulge at the front and the cleft of the seat.
  - The legs were separate tubes that had to lean in and fill out at their tops to meet that piece, which pulled them
    together just where they should part.
  - The openings left at the joins were covered one by one: a step that pressed the legs past the middle so no slit of
    light showed, a gusset, a fly panel and a levelling pass. Each fix moved the fault rather than removing it.
  - The `legs` check looked only from 15 cm below the crotch, so legs joined over the tops of the thighs passed.
- **Now (`trouserGeo`):** the trousers are cut as a pair is. Each half is one piece of cloth from the waistband to the
  hem. Over the hips and seat it lies on the hull of his body (hollows bridged) plus the ease, and below the widest point
  it falls in a line. The halves meet down the middle, front and back, and along a crotch seam 2 to 4 cm below his
  crotch. Below it each half closes round its own leg (`legSecs`), so the legs part in an arch. A leg's inside that
  would run past the middle is eased back to a narrow gap (2.5 mm a side, plus 4 mm for every 10 cm down), never onto
  his thigh (`thighGap`). The pressed seam, the gusset and the fly panel are gone.
- **Guard:** `legs` now looks from 7 to 30 cm below the crotch, wherever his own thighs (as built, Edit Dave's shape
  included) are 1.5 cm or more apart. Main fails it (`c6-denim`: 14 rays meet the trousers); this change passes.
- **Still to do (from the review of folds and fit, same day):** the cloth is still smooth, with no folds or creases
  where it bends or gathers. Shaded fold lines (a height field added to the weave's bump in the shader, so the 3D
  check's geometry is unchanged) were tried on a scratch copy: whiskers at the crotch, folds behind the knee, the break
  over the shoe. They read well and are queued in STATUS.md, with the same for sleeves and the waist of tucked shirts.

## 2zzzzzzzzzzzz. Folds and creases in every garment, a studio room's light, shade between layers (12 Oct 2026)

Emma: "make how the clothes sit on the 3D model appear more naturally like the picture in the way it has folds and
creases ... this improvement should be for all clothes and not just trousers."

- **Folds are shaded, not modelled** (`FOLD_GLSL`, `foldMat`). Every garment mesh carries a `fold` attribute: the
  direction round its own tube as a sine and cosine (a leg, an arm, his body, the shoe; outside positive), the height it
  was built at (along the shoe for a shoe) and which tube (a leg's or sleeve's side, 0 for the body). A height field over
  those is added to the normal after the weave's bump (`fPerturb`, after `normal_fragment_maps`), so the geometry, the
  layering and the 3D check see the same cloth. Each item has its own seed (`foldSeed`).
  - Trousers and shorts (`lo`): whiskers fanning from the front of the crotch, drag lines down the inner thigh, a smile
    under the seat, creases behind the knee and slack over its front, the break stacked over the shoe (crescents at
    their own tilt, never level rings), a cuffed jogger's gathers, a long drape (more on a wide leg), a pressed crease on
    tailored trousers. Settings by cut and cloth in `FU` at the call to `trouserGeo`.
  - Tops (`up`, fitted tops and the cut ones: vests, gilets, waistcoats via `foldTorso`): drag lines from under the arm
    across the chest and back, a tucked shirt bloused over the waistband, a loose top's folds up from the hem at the
    sides; on sleeves, drag lines from the armpit, bunching in the crook of the elbow, folds stacked above the cuff.
    Shirts crisp, tees and knits soft and wide, tailoring light, padded jackets none. Settings in `UT`. The sleeves'
    geometric rings (`sleeveFolds`, which read as a spring) are no longer used on the real body.
  - Shoes (`ft`): creases across the top behind the ball of the foot.
  - Trouser legs keep a little shape of their own (`legDrape`: a soft unevenness round the leg and the cloth pushed out
    over the shoe at the break) in place of the old ring folds (`legFolds`, still used by the drawn-only figure).
- **Pitfalls found on the way** (each is noted in the code):
  - Three.js's cube map code (on whenever there is an image light) `#define`s `r0, r1, r4-r6, m0, m1, m4-m6, v0, v1,
    v4-v6`. The skin shader used `r1` and `r2` as names and stopped compiling; renamed (`sk1`, `sk2`). Never use them.
  - A fold's slope is taken a hair's breadth along and round the tube and carried to the screen by the attribute's
    derivatives (`foldDH`); sampled a whole pixel away it sparkled on the small steep triangles at a crotch seam.
  - The side (±1) is rounded before it seeds the hash: interpolated, -1 came out a hair off and the hash changed pixel by
    pixel (the left leg's and left sleeve's folds were speckled).
  - The tilt a fold gives is capped (about 35 degrees) and framed by the unbumped normal (`geometryNormal`).
- **Light** (`studioEnv`): a room with softboxes (key above to his right, fill, a rim strip behind, a pale floor) made into
  image light with `PMREMGenerator`, once per renderer and light mode, from `scene.onBeforeRender`, so the live view,
  the card stills, the 3D check and the QA scripts all get it without any change of their own. The sky light, key and
  fill lamps are turned down to match (overall brightness within 2 % of before). `window.__noenv` and
  `window.__nofold` turn either off, for before and after renders from one build.
- **Contact shade** (`layerShade`): when a top is finished, the layers under it darken just below its hem (30 %, fading
  over 5.5 cm) and inside its front edges when worn open (22 %, over 3.5 cm), through the vertex shade they carry.
- **Check:** `legs` now carries its heights through Edit Dave's proportion warp (`__qa.propWarp`): measured at the built
  heights, a long-bodied Dave's band sat 5 to 7 cm too high. The 3D check on 8 outfits (`c6-denim`, `smart-casual`,
  `wk-lounge`, `g-lounge-04`, `wedding-guest`, `h10-surf`, `w20261006-casual-04`, `lazy-sunday`): nothing flagged.

## 2zzzzzzzzzzzzz. The folds still missing, and contact shade at cuffs, collars and hems (12 Oct 2026)

The follow-up to 2zzzzzzzzzzzz, from STATUS.md "Now" items 2 and 4. Shading only: no geometry moves, so the layers and
the 3D check see the same cloth as before.

- **The back of a tucked shirt** (`FOLD_GLSL.up`, under `fTuck`): a soft roll across the small of his back where the
  waistband holds the shirt down, a fainter one above it, and two short folds rising from it toward the shoulder blades.
  It was smooth from behind, the blousing only at the front.
- **A jacket's or coat's lower back** (`fBack` in `UT`: jackets 1, coats 0.9, dressing gowns 0.8, gilets 0.6, blazers 0.5,
  jacket-weight overshirts 0.6; none when tucked or padded): soft folds across the small of the back, each at its own
  slant and length, and below the seat of a long coat, long folds down to the hem.
  - **Pitfall:** anything that crosses his spine must be the same either side of it. The body's folds take a seed per
    side (`sd`), and `sin(1.7*A)` is not the same at A = pi and -pi; both left a seam down the middle of his back. Use
    whole turns of A (`sin(2.0*A)`), no side seed, and `sin(A)` as the coordinate across the back (smooth through it).
- **Scarves** (`FOLD_GLSL.sc`): the loop gets a fold attribute of its own (direction round his neck, height): folds
  running slantwise round it as wound cloth twists (7 round a scarf, 5 steeper ones round a neck warmer), and across the
  front the edge of the outer turn where it lies over the inner one (not on a neck warmer). The hash runs on
  `mod(k, fN)` so the folds meet up behind his neck.
- **The heel counter** (`FOLD_GLSL.ft`, `fHeel`, `fCtr`): the stiffened piece round the back of the heel, its stitched
  edge running from high at the back down and forward to the sole, on every shoe and boot but slippers (trainers most).
  All of the very back of the heel counts as counter: the cap closing the heel has no direction round the shoe at its
  middle, and an edge drawn across it showed as a V. (A soft V at the bottom of the heel seen from behind is in the
  last's own shape, from the cap's normals, and was there before: `upperGeo`.)
- **Contact shade** (with `layerShade`, which already shaded below hems and inside open fronts):
  - on his hands just below long sleeves (26 %, over 4 cm), and on his arms below short ones (20 %, over 4 cm);
  - on his neck just above whatever stands round it (30 %, over 4 cm), from the top of the cloth in each direction in
    the map of what he wears round his neck (`OCC.N`), so it follows a collar, a crew neck or a V. The skin's vertex
    shade is now a copy per outfit (`bodyCols` keeps one per shape);
  - on the shoe or boot under a trouser hem (`hemShade`): darker just below the hem and a few centimetres out past it,
    from the hem's outline round each leg (`HEMS`). Materials shared with pieces that have no vertex shade are copied
    first (a material told to use vertex colours on a mesh without them draws it black).
- **Before and after from one build:** `window.__nocs` turns all contact shade off, as `__nofold` and `__noenv` do;
  `QA_INIT='window.__nofold=1'` on `zoom.js` sets any of them.
- **Check:** the gate set (`tools/qa/gate.txt`) on his saved shape: nothing flagged, as before; the stored specs read
  the same.

## 2zzzzzzzzzzzzzz. Edit Dave: sliders centred on the last save; biceps, forearms, thighs and calves (12 Oct 2026)

Emma asked for the sliders to go back to the middle when she saves, so there is room to adjust either way later, on
every slider; and for thigh, calf, forearm and biceps sliders in the body section.

- **Centred on the last save** (`ceRng`, `ceBase`): every slider's middle is his look as saved (`ceSaved`, or `CHAR` when
  nothing has been saved this visit), not the fixed `CHAR_DEF`. After Save the form is redrawn, so every slider sits in
  the middle again; the stored values are the real ones, so nothing saved before changes. The middle reads "As saved".
  - The ends reach at least the usual range (-1 to 1 on the shape sliders, a slider's own min and max on the others)
    and at least a step past the middle (0.6 on shape sliders, 1 on hair, a proportion slider's own `span`).
  - **Hard limits** (`CE_LIM`): 1.8 either way on shape sliders, 2.6 on hair, 2 on proportions. Saving at one end again
    and again moves the middle out until it meets the limit, then stops. The body morphs are pushed past 1 there (at most
    1.8 times the target); at 1.8 on all four new sliders the gate set still fits (see Check).
  - Other range sliders (height, colours, amounts) keep their own min and max; the saved value is the middle, and each
    half of the slider covers the distance to its own end.
- **Biceps, forearms, thighs and calves** (`bicep`, `forearm`, `thigh`, `calf` in `CHAR_DEF`, `BODY_KEYS` and the `CE` list),
  from MakeHuman's CC0 arm and leg targets in `tools/build_body.py` (`armslegs/l- and r-upperarm-muscle`, `lowerarm-muscle`,
  `lowerarm-fat`; the thigh and calf targets were already in the build). At full slider:
  - thighs about 11 % bigger or smaller round; calves +17 % / -18 %; biceps +15 % / -12 %; forearms +25 % / -21 %.
  - The weights in `SLIDERS` were set by eye: the forearm targets at full strength looked overdone, the biceps too faint.
  - Clothes follow on their own: the new morphs go through the same sections (`secd`) and fit maps as the other body
    sliders, so sleeves and trouser legs widen or narrow with him.
- **The form:** "Size and shape" now has "Fine-tune the body" (chest, belly, hips, neck, shoulder slope, body depth) and
  "Arms and legs" (arms overall, biceps, forearms, legs overall, thighs, calves) as two folds, each remembered open or
  shut. The athletic body type now has bigger biceps, forearms and calves, and the heavier type bigger thighs and forearms.
- **To add another body slider:** add its targets and its `SLIDERS` row in `tools/build_body.py` and rebuild
  `data/body.json` with `--mh <MakeHuman checkout>` (targets from `raw.githubusercontent.com`); add the key to `CHAR_DEF`
  (0), `BODY_KEYS` and `CE`, and to a list in `CES`. `bodyW()` picks it up from `BODY.sliders`.
- **Check:** the gate set on his saved shape and on the athletic and heavier types: nothing flagged. On a test copy with
  the four new sliders at +1 (and +1.8), every outfit with trousers was flagged "sunk" on the thighs: see the next entry.
  The stored specs read the same (1381 pieces).

## 2zzzzzzzzzzzzzzz. Trousers meet where his thighs do; a clear view in the fitting room; tops no longer stand off his chest (12 Oct 2026)

- **Trouser legs and bigger thighs** (`legSecs`, `thighIn`): below the crotch each leg kept its inside 6 to 18 mm clear
  of the middle whatever his shape, so the legs parted in a V. With bigger thighs (Thighs or Legs toward the top of
  their range; the old Legs slider at +1 did it too) his thighs touch there, and his hidden thighs filled the V: the 3D
  check flagged every outfit with trousers "sunk" on the thighs. The parting now never opens wider than his own thighs
  (less 5 mm), as the inside limit in `trouserGeo` already did (`inX`, which now uses the same `thighIn`). His saved
  shape looks the same.
- **Clear view** (Emma, on the artifact: "make these buttons and the side menu able to close so i can get a better view
  of the model"): a "Clear view" button at the bottom right of the fitting room's stage (and the H key) puts away the
  pins, the buttons over the model, the side panels and the outfit strip, leaving the header (to close it) and the model,
  which grows to fill the space; "Show controls" brings them back. `FR.clear`, `frClear`, `data-clear` on `#fr`; kept on
  this device (`dw-frclear`).
- **Tops stood off his chest** (Emma: "the shirts and jumpers just stick out"). Measured against his bare body, mid-front
  and mid-back (`standoff.js` in the session scratchpad; rays at 1.32, 1.22 and 1.08 m): a tee stood 13 mm off his chest
  over the pec and 24 mm at the breastbone, 31 mm off his back and 49 mm off the small of his back; a jumper 16 mm and
  52 mm. Two causes in `fitTop`:
  - the whole of a layer's room (`e`: 8 mm base, 17 mm mid, 25 mm outer) was added all round his torso, at the chest
    and shoulder blades too, where a top rests on him. Round the torso it now gets half (padded pieces all of it, their
    bulk being the padding); its looseness still shows in how it hangs below the chest;
  - below the chest the cloth hung straight down from the widest point above, so down his back it stood off the small
    of his back by the depth of the hollow. It now spans from his shoulder blades to his seat (the upper hull of his
    profile, `HS`), 85 % of the way on the back, and is taken in 10 % at the waist (was 8 %).
  - After: a tee 6 mm off his chest over the pec, 24 mm off his back and 40 mm at the small of it; a jumper 8 mm and
    42 mm. Each layer is still kept outside the one under it (`occT`, `gp`).
  - Only base and mid layers (`F.snug`: shirts, tees, polos, jumpers; not hoodies, whose hood lies over the layer above)
    get the half, and only round the torso from the armpits down; under a jacket or coat (`F.under`) the whole room fades
    back in from 1.24 to 1.34 m (`DTF`), where the cloth meets the jacket's yoke and collar (under a knitted vest it stays
    in, or the tee came through the vest's armholes on the loose fit: g-lounge-04, front poke 66). The span down the back and the 10 % waist taper are for snug
    layers only; jackets and coats hang as before (a padded jacket pulled in over a hoodie showed the shirt collar
    through it beside his neck: w20261006-casual-04, back poke 34 on the heavier and athletic bodies). Halving the yoke and neckline too let a shirt collar show through a padded jacket at the
    shoulders on the athletic body (pull-request check, w20261006-casual-04 back poke 34); halving jackets let an open
    jacket's fronts fall behind the shirt or roll neck under them, a sliver of background between them from the side
    (mn-smart side holes 53, wedding-guest 27). Jackets still come in at the back, following the shirt under them.
- **The striped polo by the pool and its cap** (Emma, on the artifact: "no lines on the arm of this shirt as you see in
  the ad, put hat design on the cap too"):
  - the Lambretta polo is white with one navy, red and navy band across the chest; its name ("stripe polo") made it
    striped all over, sleeves and back included. A correction (`pat` plain, `front` true) keeps the photo's band and
    logo on a plain polo, and a correction saying plain now outranks a pattern the listing's name gives (`pm`);
  - a cap's design: a new correction field, `crown`, the crown seen from the front cut from the shop photo, laid over the
    front of the 3D cap (by where each point is seen from the front, fading into the cap's colour round the sides). The
    Lambretta cap now shows its red racing stripe and lettering. Not yet: the stripe over the top to the back.

- **Check:** the gate set on his saved shape, the four body types, and test copies with the new limb sliders at +1.8
  and -1.8, weight at +1.8, arms and legs at +1.8 and muscle at +1.8. Still flagged: a test body with everything pushed
  together (weight 0.6, muscle 0.6, arms and legs 1, the four new sliders 1.8): short sleeves poke at the back of the
  armpit on two outfits, a jacket on one, joggers at the shin on one. Next.

## 2zzzzzzzzzzzzzzzz. Slim, regular, relaxed, wide and baggy bottoms you can tell apart, shorts included (12 Oct 2026)

Emma, on the artifact: "make differences between baggier and slim trousers clearer. i should be able to tell how it
will fit accurately", then "include shorts and all types of bottoms".

- **One reading of the cut** (`bottomCut(p)`, `BOTCUT`), used by the 3D model, the drawing and the fitting room's words:
  the shop's `fit` (Relaxed, Regular, Wide leg, Straight) and the name give k: skinny, slim, tapered, regular, straight,
  relaxed, wide, baggy (baggy, parachute, oversized, skate, basketball) or barrel; `cuff` for a jogger gathered at the
  ankle; `flare` for bootcut and flares; `bot` for cropped. Before, the 3D model and the drawing each read the cut
  their own way, and the 3D room at the thigh only ran from 16 to 35 mm and the share of the thigh's width kept to the
  hem (`fall`) from 0.68 to 0.92, so regular, straight, relaxed and wide looked alike.
- **The spread** (`e0` room all the way down, `wide` more of it toward the knee, `fall`):

  | k | e0 | wide | fall | shorts: len below crotch, sfall |
  | --- | --- | --- | --- | --- |
  | skinny | 6 mm | 0 | 0.40 | 20 cm, 0.80 |
  | slim | 8 mm | 2 mm | 0.50 | 22 cm, 0.84 |
  | tapered | 10 mm | 6 mm | 0.46 | 25 cm, 0.88 |
  | regular | 12 mm | 4 mm | 0.64 | 27 cm, 0.92 |
  | straight | 13 mm | 10 mm | 0.90 | 28 cm, 0.97 |
  | relaxed | 15 mm | 24 mm | 0.95 | 30 cm, 1.02 |
  | wide | 16 mm | 34 mm | 1.02 | 32 cm, 1.04 |
  | baggy | 17 mm | 46 mm | 1.06 | 36 cm, 1.08 |
  | barrel | 13 mm | 22 mm | 0.60 (+18 mm at the knee) | 30 cm, 1.00 |

  A cuffed jogger tapers to 0.48 unless it says relaxed or loose. The crotch sits a little lower on looser pairs
  (`0.6*wide`), as a dropped crotch does.
- **Shorts** were all one length (29 cm below the crotch) and width. Their hem now comes from the inseam when the name
  gives one (5", 7 inch: inseam plus 1 cm), else by kind (running and split shorts 16 cm, swim 20 cm, board, basketball,
  jorts, long and knee shorts at least 36 cm) and by the fit's `len`; their width at the hem from `sfall`. The skin
  hidden under them now stops at their own hem (it stopped at the old length, so shorter shorts showed a gap above the
  knee), and a cargo pocket sits just above the hem.
- **The drawing** reads the same cut: ten leg widths at the hem (`HX`), and shorts drawn at their length and width.
- **The fitting room** says how a pair fits, by the piece's price: "Relaxed: roomy through the thigh, straight to the
  hem", "Tapered: room at the thigh, narrowing to the ankle, gathered at the ankle", shorts with their hem "about 7 in
  below the crotch" (`cutWords`).
- **The 3D check** reads where a pair of shorts ends (`loHem`, returned by `make3Dcore`) for what they cover, instead of
  assuming 25 cm below the crotch.
- **Check:** one pair of each fit rendered front and side on a plain tee (sw-chino-stone regular, js-levis-501 straight,
  wk-blaklader-1400 relaxed, wk-cernucci-cargo-charcoal wide, js-levis-578 baggy) and five shorts (hs-bb-coast-swim,
  sp-4505-7in, r11-matalan-shorts, sp-4505-cargo, wk-stanray-short-black); the stored specs read the same; the
  pull-request 3D check on all bodies.

## 2zzzzzzzzzzzzzzzzz. Garment drape upgrade: Emma's decisions, what was found, and the template builder begun (12 Oct 2026)

Emma brought a design handoff, "Dave's 3D clothing fit review" (now in `design/garment-drape/`: `README.md` is the plan,
`3D Fit Review.dc.html` the review, `Drape Test.html` with `drape.js` a working proof of concept on `data/body.json`).
It recommends replacing how garments get their shape (`fitTop`, `fitCollar`, `occPushPt` / `occAddMesh` and `warpMan`
for clothes) with patterns draped as cloth in Blender and settled in the page in wearing order, keeping the body,
Edit Dave, the photo reader, `fixes.json`, `specs.json` and the checks. This session stopped part-way, at Emma's
request, during the proof's first step. **Nothing in the page has changed.**

**Emma's decisions (asked in the session):**
- Yes to the newer Three.js (the plan's step 1) and to Blender-made garment templates (step 2). Both were listed as her
  decisions in HANDOFF.md.
- Proof first, behind a switch so the live page is unchanged, then report back before going further (the plan's
  "Proof first").
- A few seconds of cloth settle the first time an outfit is opened is fine; cards reuse the cached result.
- Dave's measurements: assume what the model has now is right, but make the sizing adjustable so she can change it.

**Found on the way:**
- **g-mod-27's "hoodie" has no hood.** `r9-dc-slell-wine` is Duck and Cover's "Slellmoore 1/4 Zip Hoodie Wine"; the
  shop's own product feed (`/products/slellmoore-1-4-zip-hoodie-wine.json`) says "quarter zip ls top, high neck
  collar, metal effect coil chain quarter zip, self fabric double fold hem & cuff band", and its photo shows a funnel
  neck. On `main` the model draws a hood, drawstrings and a full-length zip. Two faults: the outfit's piece is
  `"shape": "hoodie"` (`data/outfits-new.json`), where it should be `halfzip`; and `descOf` reads its zip as full,
  because "quarter-zip hoodie" contains "zip hood", and `D.zip` tests for a full zip before a half one. So PR #34's
  g-mod-27 failures are about a hood the garment does not have. The real hood-under-an-open-outer-layer cases are
  `w20261006-casual-04` (SikSilk full-zip hoodie under a Dickies Scobey puffer) and `hoodie-coat` (ASOS boxy hoodie
  under a long coat). Not fixed here: it is a data and listing-reader change, with its own specs and 3D check run.
- **On `main` the 3D check passes all three outfits on all five bodies** (`--body dave|slim|athletic|heavier|loose`:
  0 flags), while the renders show the hood as a flat shield on the jacket's back and a flap standing off his neck,
  and a ragged jacket collar. That is the review's point 05: the counts catch glitches, not wrong shapes.
- **His saved shape uses the proportion sliders** (legLen −0.9, torsoLen 0.38, neckLen −0.63, headSize 0.225,
  torsoDepth −0.138, shoulderSlope 0.951), so `warpMan` runs on every body, not only on Edit Dave's extremes. Under it,
  the arm and the torso move differently by up to 2.7 cm at the armpit (the shoulder slope drops the arms, not the
  torso beside them), so a template has to be bound to his body after `propWarp`, as the plan's step 4 says. Afterwards
  the page scales the whole figure by 1.79 / W(1.79) = 1.036 (times `height`/183), so a metre in the warped frame is
  0.965 of a real one; the builder sizes the cloth by that.
- **The measuring card's figures may read low.** `ceMeasure` scales the chest, waist and hips by `height`/183 only,
  not by the 1.036 the page scales him by after his proportions (nor the torso depth), so "His measurements, from the
  model" may be 2 to 3% under what is drawn. Worth checking before settling the open question of his 34 in chest
  against L tops. Not changed.

**Started: `tools/build_garments.py`** (headless Blender 4.5.14 LTS, downloaded and checked against its sha256 on first
use; run as `python3 tools/build_garments.py --only hoodie --debug <dir>`, about 2 minutes a garment):
- **His body:** `data/body.json` with his saved morphs and `propWarp` ported, reproduced from the same MakeHuman rig as
  `tools/build_body.py` (to 0.08 mm), plus A-poses at 40, 30, 20 and 12 degrees with the same vertices.
- **Patterns, size L,** in `MEAS` (cm): a front and back (the front cut in two for an open jacket), set-in sleeves whose
  cap is solved to be 3% longer than the armhole, a two-piece hood, a stand collar; rib bands drafted narrower than the
  body (`band_k`). Trued as a pattern maker would: the armhole meets the shoulder at a right angle, the neckline leaves
  it at one, and the sleeve cap leaves the underarm level, so where pieces meet their corners add up to a full turn.
  A check prints the worst corners after welding.
- **Meshing:** constrained Delaunay, 1.4 cm, seams sampled alike on both sides.
- **Placing:** the body pieces wrapped on an ellipse round his torso and bent over his shoulders, the sleeves rolled
  round each arm, each seam closed by moving both sides toward each other (nearby cloth carried along), then pushed
  clear of his skin.
- **Drape:** the seams welded into one mesh, eased to the pattern's lengths with a quick solve against his body
  (numpy), then Blender cloth with gravity, his body as a collider whose shape keys bring his arms down from the A-pose
  to his relaxed pose while the cloth follows.
- **Where it stands:** the hoodie's body drapes cleanly in the A-pose and reads as a crew-neck sweatshirt (edges within
  9% of the pattern's lengths). Once the arms are down, one diagonal fold runs from his right shoulder across his
  chest, with a pinch near the front of his left armhole. The quarter-zip (`halfzip`) and the jacket run end to end
  but have not been looked at; the quarter-zip's collar shows a +368 degree corner at the centre front. The hood's own
  drape is not written. Nothing is written to `data/garments/` yet.
- **Lessons, each of which cost a run:** Blender's gravity points down its z axis unless `scene.gravity` is set (the
  page's frame has y up), so the first drapes were pulled toward his back. Blender's `delaunay_2d_cdt` fills an
  outline's hollows (the neckline, the sleeve cap's) even with output type 1, and lays slivers of no area along
  straight edges; both stood the neckline up as a funnel. Corners that do not add up to a full turn where pieces are
  sewn stand up as funnels and "ears". Blender's sewing springs did not hold the seams closed (1.9 cm apart on average
  after the drape, 20 cm at worst), so the seams are welded instead. Blender keeps the cloth's starting creases as its
  resting bends, so the starting shape is smoothed hard first.
- `tools/garment_view.js` renders the `--debug` files (his body, the garment, sewing lines) from any angle without
  the page.

**Next, in order** (STATUS.md "Next agent, start here" has the same list):
1. Finish the hoodie: remove the fold left after the arms come down. Try more, smaller pose steps (`--frames 2`), a
   lower `bending`, or 6 to 10 frames of settle between poses.
2. The hood: its own cloth, its neckline held on the garment's (`Garment.hood_ring` pairs each half's edges with the
   garment's), placed up round his head, with gravity tilted backward for about 40 frames (for example
   `scene.gravity = (0, -6, -8)`, then `(0, -9.81, 0)`) so it falls back onto his shoulders, and the draped hoodie as a
   static collider (`static_collider`).
3. Look at the quarter-zip's and the jacket's drapes; fix the collar's centre-front corner, and stiffen the collar
   (the `stiff` vertex group, `bending_stiffness_max`).
4. Write `data/garments/<archetype>.json`: each point's position (his warped frame), the triangles, each corner's
   place on the pattern (as UVs at the page's 1.2 per metre round and 3.33 per metre down, `lookTex`), the piece of
   each point, its binding (the nearest body triangle among the allowed regions, sleeves to `uarm`/`farm`/`hand` and
   the rest to the torso, neck and head, with barycentric weights and the offset in that triangle's frame), the hood's
   pins on the neckline, the scale 0.965 and the measurements used. Keep it under about 8 MB in all (section 4).
5. The page, behind a switch (for example `window.__drape`, set from a QA script with `QA_INIT`): load the templates,
   bind them to his final body (`bodyPos()` warped as `warpMan` warps the body, with `bodyArmMask`), and settle them
   inner to outer (`layRank`) with `drape.js`'s solver against the body, the layers already settled and copies of
   the other inner pieces warped the same way. Mark the draped meshes so `warpMan` skips them. Rest lengths come
   from the pattern, graded by the size; materials from `pm(p)` with the pattern's UVs; painted folds off on draped
   pieces at first; the skin hidden from their own hems and cuffs.
6. Sizing she can adjust (her decision): the fitting room shows the garment's numbers and his model's, and lets her
   pick another size or change the numbers for a piece.
7. The proof: g-mod-27 as its data says (PR #34's case), g-mod-27 as a quarter-zip, and the hood laid over the track
   jacket, on all five bodies, `tools/qa/zoom.js` with `"0,1.22,2.9,1.18;0.785,1.22,2.9,1.18;1.5708,1.22,2.9,1.18;
   3.14159,1.22,2.9,1.18;2.36,1.62,1.2,1.5"`, beside `main`. If it does not clearly beat `main` from every angle,
   stop and report to Emma. Then the plan's steps 1 to 6 (`design/garment-drape/README.md`).

Separately, as a small data pull request (not garment geometry): g-mod-27's piece as `halfzip`, and `descOf` reading
"quarter-zip" before "zip hood". Both change renders and stored specs, so run `node tools/specs.js`, `specs_diff.py`
and the 3D check on every outfit using a quarter-zip "hoodie".

## 2zzzzzzzzzzzzzzzzzz. Garment drape proof: the hoodie fixed, the hood, three templates, and the page behind a switch (12 Oct 2026)

Continues 2zzzzzzzzzzzzzzzzz (PR #36). Everything in the page is behind `window.__drape`. Without it, the page is as on
`main`: the switch only adds the templates to `docs/data/garments/` and a few lines that do nothing while it is off.

**The hoodie's fold and pinch: four causes, none of them the arms coming down.** Rendering the drape frame by frame
(`GB_SNAPS`) showed the fold already there in the A-pose, as a tuck across the chest between the armholes:
- **His body tears at the front of each armpit.** `propWarp` moves arm vertices (`bodyArmMask`) and the chest beside
  them by different amounts. His saved shoulder slope drops the arm's skin by up to 1.7 cm more than the chest next to
  it, a ridge you can see on his bare chest. In the A-pose it lies across his chest, the cloth caught on it, and the
  tuck hung between the two ridges. The builder now blends the two warps over a few centimetres of skin (`Body.armW`).
  **The page draws the same tear** (it is under clothes, and shows on a bare chest or a vest): `warpMan` could blend
  the same way, but that moves every render and needs the full check. Not changed.
- **The relax shrank the cloth onto him.** Laplacian smoothing pulled the cloth in, and the 29 cm of ease round his
  chest gathered into fins along the side seams (folded 75 degrees, against 8 as placed). Blender kept them as resting
  creases. It is now Taubin smoothing (each step followed by a slightly larger one the other way), which does not
  shrink: side seams 9 degrees.
- **His left sleeve faced inward.** Both sleeves were cut alike and wrapped round the arms in mirror image, so the left
  one was inside out. Blender's bending measures angles by the way triangles face, so it fought a half turn all round
  that armhole: the pinch. The left sleeve is now cut mirrored, like a piece cut from folded cloth. Seams are paired
  by the pattern's own directions (pieces sewn edge to edge run opposite ways), and the build stops if any sewn edge
  joins pieces facing opposite ways. The same check then caught the collar, which was wrapped by his right first;
  it now runs by his left, and the quarter-zip collar's +368 degree corner is gone.
- **The rib hem and cuffs were steps in the side and underarm seams**, cones at each hip and wrist (the "+99 / -79
  degree" corners). They are now pieces of their own, narrower, with the body gathered into them.

Tried, and not the cause: settling between poses (`--hold`), lower bending, lower mass, lower friction, draping
straight in a lower A-pose (`--start 3`), no self-collision. The flags stay for trying drapes. Each sleeve cap now
starts as a smooth surface from the sleeve's ring up to its armhole.

**The hood** (`drape_hood`): its two halves sewn up the back and placed up round his head (an ellipsoid round his
head's skin), the neckline pinned on the draped hoodie's, then let fall with gravity tilted backward for 40 frames
and settled for 50, against his body and the draped hoodie. It ends down behind his neck, bunched as a real hood
lies, 0.0 mm off the neckline. A softer hood (`--hood-bending 0.1`) looks the same: the shape is the cut's.

**Templates** (`data/garments/<kind>.json`, 463, 417 and 441 KB): the welded points in his warped frame; the pattern
points (each with its welded point, its piece and its place on the flat pattern in metres) and the triangles over them;
each welded point's binding (its nearest body triangle among its regions, barycentric weights of its foot on that
triangle's plane, and its height along the unit normal), which rebuilds the drape to 0.001 mm; the measurements, the
cloth scale (0.965) and his shape; the hood in its own block, with the pins tying its neckline to the garment's.
At this size 45 kinds would be about 20 MB, over the plan's 8: store float16 or quantised positions before scaling up.

**The page, behind the switch** (`drapeTops`, next to `warpMan`; `QA_INIT='window.__drape=1'` for the QA scripts):
- `loadBody` also loads the templates when the switch is on. A hoodie, quarter-zip or jacket is then left out of
  `make3Dcore`'s tops (so none of its fitTop, collar, hood, bands or front details are built), and added after
  `warpMan`: each point placed on his warped body by its binding, then settled inner to outer against his body (torso
  and arms apart), the clothes under it (those `make3Dcore` built, normals turned away from his body) and the draped
  layers already settled. A hoodie's hood goes last, its neckline pinned on the hoodie's, out over anything worn over it.
- **The solver** is `drape.js`'s (position-based, distance constraints along every edge and softer ones across every
  pair of triangles), at the lengths as draped on his saved shape. **At full gravity it let the cloth slide off his
  shoulders:** at 8 iterations a step it is far softer than Blender's, and the garments ended up in a heap at his feet.
  The template is already hanging at rest on him, so each point is drawn back a little (8% a step) toward where its
  binding puts it, under a fifth of gravity. Draped layers are kept 1 cm apart: at 6 mm, the layer under showed
  through at the back of the jacket's armholes on the larger bodies. 60 steps; `__drapeSteps` and `__drapeTh` try others.
- The cloth is `pm(p)` on both sides, UVs from the pattern (1.2 per metre round, 3.33 down: untested on stripes and
  checks), normals smoothed across seams. No painted folds, no layer or contact shade, no front details.

**The proof** (`tools/qa/zoom.js` with the plan's five views, all five bodies, beside `main`):
- **g-mod-27 as its data says (hoodie under the open Ellesse jacket):** clearly better than `main` from every angle on
  every body. `main` draws the hood as a flat shield on the jacket's back and the jacket nearly closed over a strip of
  hoodie. Draped, the hood lies bunched over the jacket's collar as a real hood does, and the jacket hangs open over
  the hoodie.
- **g-mod-27 as the quarter-zip it is:** the shape is better (the funnel neck stands up inside the jacket's stand
  collar, the jacket hangs open), but the zip is missing (front details are not on draped pieces), and on the
  athletic, heavier and loose bodies a few flecks of the quarter-zip show at the back of the jacket's armholes.
- **Not yet:** Edit Dave's Cloth fit slider ("close", "loose") does nothing to draped pieces; the size cannot be
  changed (Emma's decision: adjustable sizing; the template has the measurements, the page has no control yet); the
  3D check has not been run with the switch on (its counts read `userData.kind`, and draped meshes are "drape0",
  "drape1", "drapeHood"); the binding differs from the page's body by up to 3.7 cm at the armpits, where the builder
  blends the warps and the page tears.

**Next, in order:** (1) report the proof to Emma (this section and PR #36's renders); (2) if she goes on: front details
on the draped pieces (the zip, drawstrings, pocket), laid on the cloth by pattern position rather than by `surfZ`;
(3) the Cloth fit slider and the size as rest-length scales per piece; (4) the 3D check with the switch on, and the
`under` rays generalised as the plan's step 6 says; (5) the page's armpit tear (blend `warpMan`'s arm and torso as the
builder does), with the full check; (6) more kinds (tee, jumper, shirt, coat), and float16 storage.

**Running it:** `python3 tools/build_garments.py --only hoodie --debug <dir>` (Blender 4.5 LTS is downloaded on first use;
download.blender.org refuses Python's default user agent, so the builder sends its own; or `pip install bpy` and run
the script with that Python), about 3 minutes a kind. `--reuse` takes the draped garment from the last `--debug` run to
try the hood alone. `node tools/garment_view.js <dir>/hoodie-draped.json out.png` looks at any stage (`THREE_JS=` for a
local Three.js). The page: build `docs/`, serve a copy (`tools/qa/serve.sh`), and pass `QA_INIT='window.__drape=1'`.

**Continued, 12 Oct, night (same PR):**
- **Front details on draped pieces** (`drapeDetails`), laid on the cloth by their place on the flat pattern
  (`drapeAt`: a pattern point's triangle, its place on the draped cloth and the normal), so they follow it on any body:
  a quarter-zip's zip down its collar's front edges and 18 cm of the front, its pull, a brand's chest logo; a
  hoodie's cords, kangaroo pocket (a patch of the cloth itself, raised 3 mm) with its slanted openings, and a zip where
  the listing says full zip (as `main` draws it, g-mod-27's "zip hood" reading included); an open zip jacket's teeth
  along each front edge (`make3Dcore`'s `zipT` and `zipM` words). A knit's hem band, cuffs and quarter-zip collar
  use the page's rib (`rib(p)`), as `main` draws them. Not yet: shop-photo fronts (`frontPhoto`), decals, `place` maps
  (yokes and bands by height) and stripes by height on draped pieces (stripes and checks by `lookTex` do run on the
  pattern's UVs, at `main`'s scale).
- **Size** (Emma's decision, adjustable): the fitting room's "How it's worn" has a Size row (S to XXL, as cut L) for
  the draped tops, with each one's chest and length at that size against his chest (the measuring card's figure).
  The cloth is graded round him by the chest's ratio (8 cm a size, as the charts run) and down him a third as much
  (`drapeGrade`, per edge by its run on the pattern), and stands off him by as much more (`drapeBind`). Edit Dave's
  Cloth fit grades it 4% either way. The size is worn state like the zip (`SIZEM`, `Live3D`'s `wear.size`); QA
  scripts take `window.__drapeSize`. One size for all the draped tops of an outfit; per piece is a next step.
- **Which tops are draped:** hoodies, quarter-zips, and jackets that are the template's cut (track tops, windbreakers,
  softshells, funnel-neck and zip-through jackets: not padded, denim, hooded, waxed, workwear, fleece or borg) and
  worn open (`openWorn`: the template cannot be done up; "Done up" in the fitting room draws `main`'s jacket). Across
  the outfits that is 64 hoodies, 49 quarter-zips and 24 jackets.
- **They stay in `make3Dcore`'s `up`** (marked `_drape`, not built there), so the pieces under and over them know they
  are there: a tee's sleeves under a draped hoodie's are not built, a coat over it is cut for a layer under it. Their
  meshes carry `up<k>` (the hood `up<k>o` when worn under something) as `main`'s do, so the 3D check classes them.
  Clothes `make3Dcore` builds over a draped top, and a scarf, hold it inside them (their surfaces as colliders turned in
  toward him, 2 cm reach).
- **The 3D check with the switch on** (`QA_INIT='window.__drape=1'`, now also taken by `check_3d.js`): the gate set on
  his own shape 28 of 30 clean. Flagged: **od-hike** (back poke 228: a hiking shell built by `make3Dcore` over a draped
  quarter-zip) and **q7-fairisle** (back poke 945 and `under`: the scarf, wound for `main`'s lower collar, over the
  draped quarter-zip's 7 cm funnel). On slim, athletic, heavier and loose, of the hood and layering cases:
  w20261006-casual-04 clean on all; g-mod-27 front poke 46 to 81 (the hoodie's neckline by the hood's root at the open
  jacket's collar); hoodie-coat back poke 64 to 201 (`main`'s long coat over the draped hoodie); od-hike 76 to 143;
  q7-fairisle 235 to 1113. All of them are a piece `make3Dcore` builds over a draped one: the fix is draping those too
  (coats, other jackets, scarves), not more rules. Without the switch the check is unchanged.
- **Not done, on purpose:** the page's armpit tear (it moves every render with the switch off: its own pull request,
  with the full check); more kinds (a tee, jumper or roll neck would lose its photo front, decals and `place` maps
  until those are laid on draped cloth: that comes first); compact storage (uint16 positions would take the three
  templates from 1.3 to about 0.8 MB, needed only with many more kinds).

**Continued, 12 Oct, late night (same PR):**
- **The photo reading's looks on draped cloth** (`drapeLooks`): the shop photo's own front, projected from the front
  onto the draped front piece's own triangles from the band to the neckline (the drawn pocket, cords and logo stand
  down, as `main` does); a print where the photo has it, front and back, laid through the piece's centre line (pattern
  height against height on him); a pattern laid by height by `make3Dcore`'s own `placeMap`. Seen on jb10-snikki (a
  photo front with its chest logo), fala-town (a print) and q7-fairisle (the Fair Isle yoke and hem band).
- **More layers round a draped top:** the trousers or shorts are among the clothes under it (they showed through
  q7-fairisle's hem at the back), a tool belt (`KITRE`) among those over it (jb10-snikki's pouches came through the
  longer draped hoodie; now the hoodie gathers inside the belt at his waist).
- **Artifacts:** this account cannot reach Emma's artifacts (FtdHKg is not found, 8uqcG opens read-only as another
  organisation's), so the GitHub build and the drape preview are published as their own (STATUS.md has the links).
  The preview build shows a Draped clothes switch (`build_site.py --drape`: `window.__drapeUI`), in a corner of the
  page and in the fitting room's top bar, draped to start; `docs/` has none.

**Last, 12 Oct, before merging (same PR):** four more kinds draped (`jacket_up`, `jumper`, `rollneck`, `tee`; the builder
takes garments without a hem band or cuffs), drawn only for their own cut (`drapeArch`: no knitted vests, V necks or
cardigans as jumpers, no long-sleeved tees, nothing worn open but the jacket; a track jacket worn closed uses
`jacket_up` with its zip). A ringer tee's neckband and sleeve ends take its second colour. Clothes worn over a draped top
hold in only their like (body in body, sleeves in sleeves: a down gilet's armholes drew a hoodie's sleeves to his
elbows). **Switch-on 3D check, gate set on his shape: 19 of 30 clean**; all eleven flags are small back pokes (34 to
155 px) of a draped tee or knit under a shirt, overshirt, jacket or coat `make3Dcore` still builds. A 4 cm hold-in
made them worse (reverted). The way on is draping those outer layers (STATUS.md, item 0). Merged with the switch off for
everyone; the drape preview artifact has the switch.

## 2zzzzzzzzzzzzzzzzzzz. Biceps and forearms build on the arms, within a joint limit (12 Oct 2026)

Edit Dave's extremes (STATUS "Now" 2): with weight 0.6, muscle 0.6, arms and legs 1 and the four new sliders at 1.8
all at once, short sleeves showed his arm at the back of the armpit (ca-beer-garden, h10-resort: back poke 99 to 100,
45 to 46 after the snug tops of #31). Each slider alone at its limit passed; the arm sliders added up.

- `bodyW` caps the biceps and forearm morphs so that arms plus either grows no more than `ARMSUM` (2.4): with the arms
  at 1 the biceps reach 1.4; with the arms at 1.8, 0.6; with the arms at 0 or below, their own limit (1.8). The sliders
  keep their values; the body uses the capped ones, and the clothes follow it.
- Checked: ca-beer-garden and h10-resort on that body (nothing flagged), and on arms, biceps and forearms all at 1.8
  (with n4-summer-warehouse, the muscle vest): nothing flagged. The joggers at the shin (g-lounge-04) pass since #32's
  cuts.
- **Still open:** w20261006-casual-04 on a heavy, muscular build (weight 0.6, muscle 0.6, arms and legs 1; none of the
  new sliders): the rim of the hoodie's hood, worn down, shows through the padded jacket's collar band at the back of
  his neck (back poke 33). It is there on the build before #31 too. The hood is laid over the jacket's back on purpose;
  round his neck its rim and the jacket's collar meet. Next: keep the hood's rim inside the jacket's collar (the
  neck occupancy, `OCC.N`, when the hood is placed), or the collar outside the hood.

## 2zzzzzzzzzzzzzzzzzzzz. Bottoms as the photos show them; the seat; a polo's own collar (12 Oct 2026)

Emma, on the artifact, after #32: "this looks hugely baggy and wrong" (a mix card), "shorts are shown more flared than
they should be, ensure we dont inaccurately represent clothes on the 3d model", "make straight, skinny, flared, baggy
bottoms clear based on the advertisement", "bum in clothes appears to be rather flat compared to the unclothed version",
and on the polo in m5-under-60: "collars still appear a bit overlapped and dettached from shirts".

- **Baggy and wide legs swelled into a bell from the side.** Each leg kept the depth of the deepest section above it,
  his seat, all the way down, and #32's wide and baggy room and `fall` over 1 added to it. A leg now takes its depth
  from his thigh (`legSecs`: `mz` from 7 cm below the crotch, 13 cm on shorts); wide and baggy have less room (wide
  `wide` 0.028, baggy 0.036) and no flare at the hem (`fall` 1). Compared with the shop photos of asos-weekday-baggy,
  uq-barrel, mt-jeans-vintage, folkclothi-barrel-leg-trouser-ecru-twill and js-levis-578: wide straight tubes, the
  barrels curving at the knee.
- **Shorts flared:** `sfall` is now 0.82 to 1.0 (wide and baggy shorts as wide at the hem as at the thigh, no wider), the
  hem's own flare halved (3 mm), and their depth from the thigh, not the seat.
- **The seat:** measured over one buttock, his bare seat stands 41 mm behind the back of his thigh; in straight jeans
  it stood 30 mm, the cloth 12 mm off the seat and 24 mm off the thigh. The cloth from the waistband to the crotch could
  only come in 0.3 m per metre going down (`trouserGeo`'s hang), so it fell straight from the seat's fullest point; on
  the back of a fitted pair it now comes in as fast as the cut allows (`o.seat`: skinny 1.6 to straight 1, relaxed
  0.6, wide 0.35, baggy 0, added to 0.3), the room round the seat goes by the cut (6 mm skinny to 15 mm baggy, was 13
  mm for all), a fitted leg's depth is not carried down from the seat (the upper hull of the leg's depth leaves out
  the rows within 9 cm of the crotch), and regular and straight have a little less room at the thigh. Jeans now: 10 mm
  off the seat, 20 mm off the back of the thigh.
- **A polo's collar** was a shirt's collar laid on a polo: long leaves standing 8 to 20 mm off the stand, ragged where
  they met over his shoulders, detached from the polo at the back and sides. A polo now has its own: a ribbed band
  (`rib(p)`) 22 mm high at the front, 30 mm at the back, folded over once, lying on the polo (`out` 2 mm) with short
  points (`front` 20 mm, `spread` 0.1), its tipping on the edge. A shirt's leaf also lies closer (`out` 3 mm, was 8).
- **Check:** m5-under-60, h7-beach-50, hoodie-coat, barrel-navy, x11-matalan-casual and h7-lambretta-pool on his
  shape: nothing flagged; the pull-request check on all bodies.
- **Still to do (photos):** reading a pair's cut from its shop photo itself (the width of the leg at the hem against the
  thigh, on a flat-lay) rather than from its name and fit label; most photos are on a model, so this needs the
  photo reader's leg outline first.

## 2zzzzzzzzzzzzzzzzzzzzz. Every pair's cut read from its shop photo (12 Oct 2026)

Emma, on x11-matalan-casual: "make straight, skinny, flared, baggy bottoms clear based on the advertisement". The cut
was read from the shop's fit label and the name; many names say nothing ("Trousers", "Chinos", "Jeans") or mislead
(cargo and work words read as relaxed, "baggy" on what is a wide straight leg).

- **Measuring the leg from the photo did not work.** A prototype outlined the leg in each photo and compared the hem's
  width with the thigh's; most photos are on a model (crossed legs, a step, cropped at the knee, busy backdrops), so
  half the readings were wrong. Dropped.
- **Read by eye instead.** Every bottom worn in an outfit (318: 240 trousers and joggers, 78 shorts) was laid out on
  contact sheets of its shop photo with the page's reading, and checked. 166 read differently and are in
  `data/cuts.json` (`"<item>": "<cut> [flags]"`): 38 straight (jeans, cords and chinos read as regular, workwear read
  as relaxed), 30 slim (tailored and smart chinos), 23 wide (painter and skate pants read as relaxed, "baggy" names that
  are wide straight legs), 22 tapered (cuffed joggers and military chinos read as relaxed), 19 relaxed, 8 baggy, 8
  regular; flags `cuff` (gathered at the ankle), `open` (an open hem on a jogger), `long` (shorts to the knee or
  below, 4 pairs). Shorts: 11 read slimmer or wider than their names.
- **Wiring:** `tools/build_site.py` checks each entry (a known item, a known cut, known flags) and puts it on the item
  as `cut`; `bottomCut` uses it over the name: the cut, then the flags (a photo-read jogger keeps its cuff unless it
  is straight, wide or baggy or says `open`). The 3D model, the 2D drawing and the fitting room's words all follow.
- **Check:** every outfit with a changed pair (321) on his shape and the heavier body: nothing flagged; the
  pull-request check on all bodies. Stored specs unchanged (they do not hold the cut).
- **New picks** are read from their name until someone adds them to `data/cuts.json` (CONTRIBUTING, "The cut of
  trousers and shorts").
- **A polo under a closed layer** keeps the low stand it had before (the new folded rib collar is for a polo on top):
  the pull-request check found the band's taller sides showing between a hoodie and its hood (g-job-06 on the loose
  fit, front poke 32; a trouser cut change brought it into the check).

## 2zzzzzzzzzzzzzzzzzzzzzz. Collars attached to their tops; necklines over necklines (12 Oct 2026)

Emma (n4-under-60 ringer, and on PR #33's renders): "collars still appear a bit overlapped and detached", then "it
still looks layered and like there's overlap that looks like misrendering at the collar".

- **Collars grown from the top's own neckline** (05efecd): the neckline used to sit at one height all round, below the
  tops of his shoulders beside his neck, so every collar grew out of a trough behind the cloth's crest. It now rises
  there to the base of his neck (`yokeCol`, `YT` in `fitTop`); `fitCollar` grows the band at right angles to the
  neckline and evens out only how far it is pushed; a ringer's colour is the tee's own neckband (`ringM`).
- **That broke layered necklines.** The pull-request check flagged g-quiet-13 (a polo under a half-zip under a gilet)
  on three bodies: the half-zip's collar stood 3 to 5 cm off his neck at the sides in wings, with a ledge where it
  met the front, and the polo showed inside it. Switching each layering rule off in turn found the cause: the
  half-zip's neckline was placed outside the furthest cloth under it at its height (`OCC.N`), and with the necklines
  raised that is the top of the polo's shoulder, not its neckline. Fixed at the rule:
  - necklines are placed from a neck-only map, `OCC.NC` (cloth within 10.5 cm of the neck's axis, as `ownNeck`
    already did for a top's own collar). Collars still clear `OCC.N`: read from the neck-only map, the hood's rim of
    w20261006-casual-04 came through the padded jacket's collar (back poke 72 to 115);
  - a neckline is never lower than the raised neckline of the top under it (`NUP`): a half-zip over a polo stayed
    up to 2.5 cm lower behind his shoulders;
  - a shirt or polo under a closed half-zip, roll neck or hoodie keeps a low band for its collar (`cov`): none of it
    shows, and its taller stand pushed the outer collar off his neck.
  Tried and dropped: measuring the neckline's rise on his body alone (the yoke then climbed over the polo again),
  hugging the hidden stand closer (no change), and limiting the sample below the neckline (halved the wings only).
- **The waistband** (g-lounge-06 tucked in, front poke 37): when the trousers' room went by the cut (2zzzzzzzzzzzzzzzzzzzz)
  the waistband stayed at the loosest cut's, 5 mm proud of a tapered pair, and came through the jumper over it. It
  now lies on the trousers at their own room (`eW`).
- **Check:** the gate set and every outfit the change touches, on all five bodies and both "How it's worn" passes (the
  pull-request check), and the stored specs (1381 pieces, none read differently).
- **From the artifact's comments, the same day:** the rendered checks passed, but close up the collars were wrong.
  - Every crew neckband (tee, jumper, oversized tee) rose up the sides of his neck in horns, with gaps at the back
    corners: the neckline was raised 3.5 cm over a few degrees where the cloth crested beside his neck. The crest came
    from the neckline being put on the neck's oval, which beside his neck lies inside the slope of his shoulders. The
    neckline now lies on his body where that is wider (up to 2.5 cm out), and the rise left is spread round his neck.
    Tried and dropped: capping the rise at 6 or 10 mm (gaps stayed at the back corners), spreading it over 70 or 90
    degrees without the averaging (a V at the back between two horns).
  - Polo collars stood as a ribbed band with box corners: a lower stand and a longer leaf with spread points now.
  - Open jackets (the Harrington, the wool-look jacket): the collar points meant for the 2D figure were laid on the
    cloth under the jacket and came through on one side as a dark flap below the collar. Drawn only without the fitted
    top now; the fitted collar's leaf falls further and spreads to points beside the opening instead.
  - The knit zip overshirt (filed as a cardigan) had no collar; a cardigan named as an overshirt gets a shirt's.
  - A scarf's loop was measured against the top of his shoulders and lay over them as a flat cape; it is measured
    against the cloth round his neck now, a little fuller.

## 2zzzzzzzzzzzzzzzzzzzzzzz. PR #33 and #34 brought back onto main; a hood laid over a jacket (13 Oct 2026)

PR #33 and PR #34 were closed unmerged when the drape proof (PR #36) went in, and Emma's artifact was republished from
`main`, which rolled their fixes back on it. Emma chose to bring them back first, fix #34's two red checks, then go on
with the drape. Their eleven commits were merged onto `main` (the drape code and theirs live side by side in
`page.html`; STATUS and this file kept both sides' notes).

- **The hood over an open jacket** (g-mod-27, back poke 57 to 157 on every body; w20261006-casual-04 on slim,
  heavier and athletic; hoodie-coat on heavier). Close up, the jacket's neckline stood 5 to 9 cm up his neck at the
  sides in wings, and its collar crossed the top of the hood. Measured per piece (`YT` against `F.ytop`): every top's
  neckline rises about 3.7 cm at the sides for his shoulders and half a centimetre more for each layer under it, but a
  jacket over a hoodie rose 5.5 to 9 cm. Its yoke lay on the hoodie's hood rim, which stands up round his neck, and the
  neckline climbed after it (#34's raise). Fixed at the rule:
  - a collar that stands (`fitCollar`'s `stand`, the hoodie's hood rim) is left out of the yoke map (`OCC.Y`, mesh
    flag `noOccY`), and stays in the neck maps, so what is worn over it still goes round it: the jacket's neckline now
    rises 4.7 cm, as over any other knit;
  - a hood laid out over a jacket presses the jacket's collar down at the back and sides, to a fifth of its height,
    rising to full height at the front (`HOODO`, set once `hoodDown` has run, read by `hAt` in `fitCollar`).
  Tried first: lowering the collar alone (the poke doubled, as the hood rim then showed between the jacket's wings and
  the hood), widening where it is lowered (no change: the wings were the neckline, not the collar).
- **The scarf check** (g-outdoor-05 "under" 3 to 4 on heavier and loose): a ray from behind passed over the back of
  the scarf, through his neck, and met the front of his neck from inside, where the jacket's collar is inside the scarf
  as it should be. `tools/check_3d.js` counts only hits before the ray reaches the middle of his neck.
- **Still open:** jb-wet-day (a hoodie's hood out over the waterproof jacket, back poke 82 to 142, red on `main` too,
  not among the pull-request check's outfits): the jacket's back shows through the top of the hood, so the hood's
  estimate of how far out the jacket sits (`eTop`, `hOut`) is short there.
- **Check:** the gate set and every outfit the change touches, on all five bodies and both "How it's worn" passes,
  and the stored specs (1381 pieces, none read differently).

## 2zzzzzzzzzzzzzzzzzzzzzzzz. Draped shirts: a point collar folded over its stand, worn open or done up (13 Oct 2026)

The first outer layer draped (STATUS.md item 0.1), behind the drape switch as before: the page is unchanged without it.

- **The builder** (`tools/build_garments.py`): `shirt` (worn open, its front in two) and `shirt_up` (done up), 110 cm
  round the chest and 79 cm long (a shirt covers a tee's hem), buttoned cuffs a little narrower than the sleeve. The
  collar is a 3 cm stand on the neckline and a leaf (`leaf`) sewn along its top, folded down over it. The leaf is cut as
  part of a ring, its outer edge 8% longer than its neck edge, deeper toward its points (4.5 cm at the back, 7 at the
  points), so folded down it lies round the base of his neck; `close_seams` places it folded, each point by its angle
  round the ring along the stand's top and down from there. It stops 1.5 cm short of each front end of the stand (the
  stand's top is cut in three for it): sewn along all of it, the two points met in one point at his throat. At 14% the
  leaf rippled along the back. About 3 minutes a kind in Blender; the fold holds through the drape and the arms coming
  down.
- **The page:** a shirt worn open is drawn from `shirt`, done up from `shirt_up` (`drapeSplit` for the templates cut in
  two). Not draped: band, grandad, camp or Cuban collars, short sleeves, a jacket-weight overshirt (a chore jacket or
  shacket), and any top tucked in (the templates hang loose to the hem; `make3Dcore` tucks it). The placket's two
  lines of stitching and buttons every 9 cm (a shade of the cloth, pearl on white) and one on the stand, drawn on the
  cloth (`drapeDetails`).
- **Layers:** a top is now draped only when everything worn over it is draped too: `make3Dcore`'s tops are cut for its
  own closer inner layers, and over draped cloth they let it through at the back and shoulders (barrel-chore: a draped
  tee through a chore jacket). A shirt's collar leaf is left out of what the layers over it lie on and is settled
  again afterwards, out over them, as a shirt collar lies over a crew jumper's neckline (`drapeLeaf`): settled under
  the jumper, it came through the jumper's shoulders. At 114 cm round the chest the shirt came through a draped jumper
  (116 cm, the layers kept 1 cm apart) at the belly and back; at 110 it stays inside.
- **Held in under what is worn over it:** after every draped layer has settled, from the outside in, each one under
  another has a short settle (20 steps), its body against the bodies over it turned in; then a shirt's leaf is laid
  out over them. (Held in by the whole of the jumper, the shirt's sleeves were pressed into the crease between the
  jumper's sleeve and its side and showed there: m5-argyle front poke 54 on his shape, 108 on slim.) A jumper's rib band gathers it in at his hips over a shirt hanging straight, and
  white flecks of the shirt came through above the band (m5-argyle front poke 34); held in, the shirt is drawn in under
  the band. The photo's looks and front details are laid after this, on the cloth as it finally lies.
- **Switch-on 3D check, gate set and five shirt outfits on his shape:** 28 of 30 clean before the leaf change (from 19
  of 30 on the gate set alone): m5-argyle was the shirt's leaf, and q7-fairisle's "under" (a draped half-zip's collar
  over PR #34's tighter scarf) is not the shirt's: it flags without the shirt templates too.

## 2zzzzzzzzzzzzzzzzzzzzzzzzz. Draped gilets, and collars and belts under a draped top (13 Oct 2026)

The next outer layer (STATUS.md item 0.1), behind the drape switch: the page is unchanged without it. Gilets were the
outer layer that kept most draped tops from being draped: 35 outfits had a draped top under one (40 gilets in the
outfits, none worn open). Next by that count: padded and puffer jackets (21) and the other zip jackets (21).

- **The builder** (`tools/build_garments.py`): a sleeveless archetype (an entry in `MEAS` with no `sleeve` skips the
  sleeves, cuffs and their seams; the armholes stay open edges) and `gilet`: a bodywarmer done up, 124 cm round the
  chest and 69 long (size L), armholes 27 cm deep and cut in to the point of his shoulder (shoulder 43 cm) so the
  sleeve of the top under it comes through, a 3 cm hem band (gathered to 0.92), the zipped jacket's 6.5 cm stand
  collar. About a minute in Blender. Corners where pieces meet +33 degrees at most (the zipped jacket's are +37); bound
  25 mm off his body at the median. `jacket_up`, rebuilt after the change, is byte-identical to the one on `main`.
- **The page:** `DRAPEK`/`DRAPEF` take `gilet`; `drapeArch` leaves hooded and tailored gilets to `make3Dcore`, and one
  worn open keeps its shapes as before (only a jacket's and a shirt's templates open). The zip from the collar's top to
  the hem as on `jacket_up`; a work or utility bodywarmer's patch pockets (`make3Dcore`'s rule); no photo front (as
  `make3Dcore`); prints as on any top.
- **A stand collar done up over a shirt** (gilet, zipped jacket, half-zip, roll neck: `STANDC`): the shirt's collar
  leaf stays inside it, held in by the whole of that layer turned in (`inCol`), as it is worn. Laid out over it (as
  over a crew jumper's neckband), the gilet's 6.5 cm collar came through the leaf (errands: front poke 142).
- **A polo's or shirt's collar built by `make3Dcore` under a draped gilet or zipped jacket** is the low band it is
  under a half-zip or hoodie (`stC` sets `cov`): its leaves lying out came through the gilet's neckline at the front
  (g-job-13: front poke 107, now 6).
- **Belts:** a plain belt is under every draped top (`drapeTops`' `under`; tool belts stay over): a draped top is never
  tucked, so the belt is under it. Left out, the belt came through the gilet at his waist (q13-coastal, front poke 224
  before the collar rule, 101 after it, clean with it).
- **Switch-on 3D check of the 40 gilet outfits on his shape** (`QA_INIT='window.__drape=1'`): 15 flagged at first,
  every one at the neck or waist; after the three rules above, 29 of 40 are clean (the 25 clean at first
  still are). Left: eight at the base of his neck (front poke 38 to 83: the top under it seen inside the gilet's stand
  collar; a roll neck there looks right close up, a shirt's leaf held inside it is crumpled), g-outdoor-21 (a
  borg-lined overshirt built by `make3Dcore` comes through the gilet's back: back poke 619), g-job-13 (back poke 40)
  and g-quiet-29 (back holes 29). The pull-request check, with the switch off, is unchanged.

## 2zzzzzzzzzzzzzzzzzzzzzzzzzz. Jackets and coats rest on his chest; scarves that hang like scarves; what other fitting tools do (13 Oct 2026)

Emma, 13 Oct: "the issues with scarves", and "still the odd 3D model that shows the chest with a protruding chest with
the clothes on despite the model being the correct size". Both are fixed for the live page (with the drape switch off;
with it on they look as right, see the end). The way each was found, so the next one can be found the same way:

**The protruding chest: outer layers stood 2.5 to 3 cm off what was under them over his chest.**
- *Measured, not eyeballed.* A scratch probe built every one of the 582 outfits and cast rays from the front over his
  chest, comparing the outermost top with his bare body (`make3D([])`). Tees, polos and jumpers sat 1.0 to 1.4 cm off
  his skin at the chest (median, by outer piece); **jackets (148 outfits) 3.9 cm, coats 4.3, blazers 3.3, dressing
  gowns 3.9, padded gilets 4.6**, up to 5.8 cm. A brown wool-look jacket over a jumper (q8-wool-jacket, the outfit
  Emma's comment of 12 Oct was on) stood 2.6 to 2.8 cm outside the jumper all down his front, and from the side and
  three-quarters its front swelled out in front of his armpits like a pigeon chest. With the painted folds and contact
  shade off (`__nofold`, `__nocs`) it looked the same, so it was the shape, not the shading; the jacket over the tee
  alone did it too, so it was the jacket's own shell.
- *Why.* `fitTop` gives each layer a room `e` round his torso (8 mm base layers, 17 mm mid, 25 mm outer, plus 4 mm per
  layer under it) measured from **his body**, not from what is under it. PR #31 (2zzzzzzzzzzzzzzz) halved it for shirts,
  tees and jumpers ("the shirts and jumpers just stick out"), but left jackets and coats with all of it: halving them
  all round let an open jacket's fronts fall behind the shirt and roll neck under them (mn-smart, wedding-guest, side
  holes 53 and 27).
- *The rule now* (`fitTop`, `F.rest`, set for outer layers): an outer layer that is not padded gets half its room over
  the front of his chest and belly (full at the front, fading out between 35 and 70 degrees round toward his sides, and
  above 1.40 m toward the shoulders), so it rests on what is under it as a real jacket does, and keeps all of it at his
  sides, back and shoulders, where its looseness shows. Padded pieces keep all of it (their bulk is the padding). It
  still stays outside every layer under it (`occT`). A jacket over a jumper now sits 1.8 to 2.2 cm off his skin at the
  chest (about 1 cm over the jumper), from 3.3 to 3.8.
- *And the edge rule that the first try lacked:* an open front that rests on his chest still reaches as far forward
  as what shows between its edges (the furthest forward point of the layers under it across the opening, plus 8 mm,
  lifted at the edge and easing back over 23 degrees), so from the side nothing under it stands proud of its edge.
  Without it, wedding-guest's tie showed past the blazer's edge from the side, as in PR #31's try.
- *Checked:* every outfit with a jacket, coat, blazer or gown (176), on his shape, against `main`: the same 3 flagged on
  both with the same counts (jb9-wet-dealer, jb-wet-day and jb8-wet-day, back poke 85: the hood over a waterproof jacket,
  STATUS "Still open" item 1), 173 clean, nothing new. The pull-request check (gate set and changed outfits, five bodies,
  both "How it's worn" runs) is green.
  Close-ups of q8-wool-jacket, festival (a long coat), g-outdoor-16, mn-smart and wedding-guest from the front, three
  quarters and side: flatter fronts, no dome in front of the armpits, nothing showing past an open edge.

**Scarves: two planks and a ruff.** Every one of the 8 scarf outfits drew the scarf's ends as boxes stacked from his
neck to the middle of his chest: two flat, hard-edged planks, half as long as a scarf's ends hang, overlapping in the
middle, splitting into steps from the side, with six sticks for a fringe. The shop photos (`tools/qa/multi.js`) show
long soft ends to the waist, worn once round, fringed, and two of them patterned.
- *The ends now* (`make3Dcore`, the scarf): each a band of cloth 11 cm wide with a 6 mm thickness (face, back, sides
  and lower edge), from under the loop to 44 cm (the longer, his right) and 36 cm (the shorter, laid over it) below it,
  gathered to 72% of its width where it leaves the loop. It lies on what he wears, read from the clothes' front depth map
  (`rayZ`) and by a ray at what is laid on the cloth (zips and their pulls, buttons, pockets, collar points; a half-zip's
  pull came through the scarf), is stiff across (bridges a gap or a jacket's edge, its sides falling back at most 8 mm
  with the curve of his chest) and hangs: going down it never comes back in toward him, so below his chest it falls
  straight, as cloth does. Each column starts just inside the loop's lower edge above it (`footAt`), and where the loop
  lies over the clothes the end is tucked behind the loop's front, so it comes out from under the loop (an end laid on a
  half-zip's collar stood out in front of the loop; one cut square from the middle showed its top under the loop beside
  it). A fringe of 16 or 17 loose strands per end, 5 to 6.4 cm, hanging straight down (crossed quads, so they show from the
  side too).
- *The loop:* its top edge rolls over toward his neck (a 5 mm half round), so it reads as a fold of knitted cloth rather
  than a cut sheet; its lift onto the clothes under it takes the middle of each column and its four neighbours first,
  so a lone column lifted onto a jacket's collar between columns that fell through its open front no longer stands up as
  a tooth; over the front of his throat its lower edge is averaged over about 55 degrees, so the ends hang from one smooth line.
- *Designs:* a new correction field, `strip` (fixes.json, checked by `build_site.py`, read by `normFix`, loaded by
  `trueFor`): one end of the scarf cut from the shop's flat-lay photo, turned upright and cropped from just above the
  fringe, laid along each end (the shorter shows its lower part). Pretty Green Rainsford (gold stripe, "PRETTY GREEN",
  the logo above the fringe) and Urban Excess No Problemo (its lettering over the glitch knit) now wear their designs;
  both were plain. CONTRIBUTING.md's table has the field.
- *Checked:* the 8 scarf outfits close up at the neck (front, three quarters, side, back) and full length, and the
  3D check of all 8 on the five bodies against `main`: clean on every body (`main` flagged g-quiet-30, side holes 26
  and 30 on the slim and loose bodies). A neck warmer (snood) is unchanged: it has no ends.
- *Not done:* the loop's top still flares over a high jacket collar at the sides (pub-lunch), as it must stay outside
  the collar (`under`); the loop stays in the scarf's main colour (a `strip` scarf's stripe is not carried round it);
  the WoolOvers scarf has only a lifestyle photo.

**With the drape switch on** (`QA_INIT='window.__drape=1'`): q8-wool-jacket's jacket rests over the draped jumper with
nothing coming through, and q7-fairisle's new ends lie over the draped half-zip. The drape's own check was not re-run.

**What other fitting tools do, and what it means here** (research for Emma's question, 13 Oct):
- *Clothing CAD (CLO 3D, Marvelous Designer)*: garments are sewn pattern pieces simulated on an avatar, each fabric with
  a collision thickness (CLO's default: 1.5 mm each side of the cloth) and the avatar with a skin offset (3 mm); layers
  are ordered by a layer number and settled in order. So a real tool keeps cloth a few millimetres from what is under
  it, never centimetres: the drape plan is the same idea, and the `rest` rule above is the closest the old builder can
  come to it. Virtual try-on shops model a scarf once in CLO on the avatar, skin it to the body and ship the mesh
  (WANNA's scarf pipeline), rather than building it from rules.
- *Daz Studio*: clothes follow body morphs by projection and are pushed off the body (or off a lower layer, the
  "collision item") by a smoothing modifier with collision iterations: a per-layer collider, as `drapeTops` does.
- *Game engines (Unreal, Unity)*: a scarf's hanging ends are cloth simulated against capsules on the neck and torso,
  attached at the loop; cloth only collides with what it is told about.
- *The in-page solver*: position-based dynamics softens as the iteration count drops, which is why `drapeTops` needs
  its pull back to the binding. XPBD with small substeps (Macklin and others, "Small Steps in Physics Simulation", 2019:
  many substeps of one iteration each) gives stiffness that does not depend on the iteration count; GarmentCode's
  simulator (NVIDIA Warp) uses it. Worth trying before more kinds are draped.
- *Pattern drafting*: GarmentCode / PyGarment (ETH Zurich; GarmentCodeData, ECCV 2024) is an open-source library of
  parametric sewing patterns (shirts, jackets, trousers and more) made to measure from body measurements; it could
  supply `build_garments.py`'s patterns instead of drafting each archetype by hand.
- *Research on layering*: ContourCraft (SIGGRAPH 2024) and ISP (NeurIPS 2023) resolve intersections between garment
  layers; HOOD (CVPR 2023) loose garments. They are learned and posed; for one pose, settled offline in Blender and
  lightly in the page, the drape plan is the practical route.
- *So, in order:* a scarf template in the drape (a long rectangle wrapped once and tacked at the crossing, settled last
  over every layer), then XPBD substeps in `drapeTops`, then patterns from PyGarment for the remaining ~35 archetypes.

## 2zzzzzzzzzzzzzzzzzzzzzzzzzzz. A draped scarf, behind the drape switch (13 Oct 2026)

The first of the next steps named in 2zzzzzzzzzzzzzzzzzzzzzzzzzz (Emma, 13 Oct: "merge and start"): the scarf as a
draped garment, settled last over everything he wears. **Behind the drape switch: with it off (the live page) nothing
changes.** PR #41.

**The template** (`tools/build_garments.py --only scarf`, `data/garments/scarf.json`, 87 KB):
- A scarf is not sewn: a band 180 x 14 cm (a 28 cm scarf folded along its length, as it is usually worn) is laid once
  round his neck with both ends down his front, the longer end 10 cm longer (`SCARF`, `scarf_path`), over his body and
  the draped jumper (a stand-in for what he wears under it), and let fall in Blender for 90 frames (about 30 s).
- *Four tries, three things learnt* (each from `garment_view.js` renders of the `--debug` stages):
  - a loop level all round, at the height of the base of his neck, squeezed its front between his chin and chest where
    both ends leave it, and it heaped up over his chin. It now dips at the front onto the top of his chest (5 cm lower
    than behind), as a scarf wound once round lies;
  - a loop 66 cm round slid down onto his shoulders like a cape and the ends piled up on his chest; at about 55 cm it
    holds;
  - left free, the back of the loop slid down his neck and, the loop being closed, drew the front up over his chin
    (frame 10 looked right, frame 30 had the heap). The upper edge of its first turn behind his neck is held where it is
    laid (a pin group), as a scarf's grip on a collar holds it.
- Still: the cloth bunches where the two ends cross on his chest (it reads as a loose knot), and the loop stands high
  behind his neck. A shorter overlap at the front moved the bunching to one side rather than removing it (tried, not
  kept).

**The page** (with `window.__drape`):
- `make3Dcore` leaves a scarf (not a neck warmer, which keeps its own) to `drapeTops` (`dScarf`), which draws it last of
  all: bound to his body, settled against every top under it, draped or not, kept **1 cm** off them (at the 4 mm the
  draped tops use against `make3Dcore`'s clothes, a jacket's toggles came through its ends; 1 cm is what the draped
  layers keep off each other), then **pushed out in front of thin details by rays**: down his front from in front, round
  his neck from outside toward it, five rays about each point (7 mm apart), only where the point is the scarf's own front
  layer (the page's cloth has no collision with itself, and an end under the other came through it when moved), then a
  short settle. Toggles, an open front's edge and a stand collar's tip behind his neck are too thin a scatter of points
  for the settle to hold the cloth out.
- `drapeScarf`: the band in the scarf's colour, each end in its `strip` design (from the foot up 44 cm, as the live
  scarf), and a fringe at each foot.
- *Checked, switch on, the 7 outfits with a draped scarf on the five bodies, against `main` with the switch on:*
  | body | `main`, switch on | this, switch on |
  | --- | --- | --- |
  | his shape | g-outdoor-05 back poke 473 | g-outdoor-05 back poke 425, **under 4** |
  | slim | g-outdoor-05 back poke 60 | g-outdoor-05 back poke 66 |
  | athletic | q7-fairisle belly skin; g-outdoor-05 back poke 336 | q7-fairisle belly skin; g-outdoor-05 back poke 281 |
  | heavier | q7-fairisle and q8-morden belly skin; g-outdoor-05 back poke 34, under 3 | the same skin; g-outdoor-05 back poke 34 |
  | loose | g-outdoor-05 back poke 598 | g-outdoor-05 back poke 598 |

  The back pokes are a draped hoodie's hood coming through the jacket `make3Dcore` builds over it, and the belly skin
  is the draped knits being short over a bigger belly (both STATUS item 0, on `main` too). The one new flag:
  g-outdoor-05 "under 4" on his shape, a single speck of the jacket's stand collar tip at the scarf's top edge behind
  his neck, where the edge folds in toward his neck (close-up renders: the rest of the back is clean). q7-fairisle's
  "under" (STATUS item 0) is clean with the switch on, on `main` too since PR #40's live scarf.
- *The pull-request check (switch off)*: green; the live page is unchanged.

## 2zzzzzzzzzzzzzzzzzzzzzzzzzzzz. Emma's comments: dark jeans, straight and relaxed legs, cuffs, four designs from the shop photos (13 Oct 2026)

Nine comments on her artifact (FtdHKg, v45), each answered in its thread.

**Trousers.**
- *m5-under-60, "colour of these trousers is wrong".* The Matalan jeans' photo reads near black (#161719), outside the
  dark wash's range, so the denim rule put the dark wash's mid indigo (#2c3d5e) in its place, which the studio light drew
  a bright blue. A general fix was tried first: keep the reading's own depth, clamped into the wash's range, in the
  wash's blue. `dump.js` before and after: 23 readings moved, 14 of them on items without a fixes.json colour, and 6 of
  those came out further from their photo (dark indigo jeans read just as near black as a rinse does; a light wash read
  grey). Reverted, as the rule says; `mt-jeans-straight` has a fixes.json `col` (#222a3a, the lit cloth in its photo).
- *m5-under-60, "slightly flared when they're straight leg"; x11-matalan-casual, "balloon a bit too much outwards
  below the crotch line".* Measured on his saved shape (a probe reading the trousers' mesh, its width and depth at 12
  heights): round the leg, straight came out 3% wider at the knee and hem than at the thigh, relaxed 15%, wide 19%,
  baggy 25%. Two causes: 12 Oct's numbers, which made the fits tell apart, let the room grow below the thigh (`wide`)
  and kept nearly all of it to the hem (`fall` 0.9 to 1); and the hem's own fullness, 12 mm front to back over its
  last 15 cm, was carried up the shin by the hull as a cone. A real straight leg is about 70% of the thigh at the knee
  and hem; on his body the knee and calf hold it out. Now (`BOTCUT`): straight `wide` 0.004, `fall` 0.82; relaxed
  `e0` 0.017, `wide` 0.01, `fall` 0.82; wide 0.018 and 0.95; baggy 0.024 and 0.97 (skinny to regular unchanged).
  Round the leg against the thigh, at the knee and the hem: straight 0.94 and 0.89, relaxed 0.99 and 0.94 (1.5 cm more
  round the thigh than straight), wide 1.08 and 1.07, baggy 1.13 and 1.12. The hem is fuller by 1.5 mm across and 6 mm
  front to back, set back 16 mm (was 4, 12 and 10), so its back edge is where it was and the heel stays inside. The
  x11 joggers were `wide` in `data/cuts.json`; their name says relaxed straight and Emma says relaxed: `relaxed open`.
- *s10-admiral, "tracksuit bottom material looks like leather and it's unclear when something has elasticated bottoms
  vs straight / baggy leg opening".* "SikSilk" matched `/silk/` in `descOf`, so all 8 SikSilk pieces were satin
  (roughness 0.42, shiny): now `/satin|\bsilk/`. The SikSilk smart joggers have an open hem in the photo (`cuts.json`
  `tapered open`). A cuffed jogger only had its hem raised off the shoe, so a relaxed or baggy pair with cuffs hung open
  at the ankle. Now the leg gathers into a 5 cm rib cuff round his ankle (`legSecs`, after the hull, which would bridge
  it), the cloth just above standing out over it a little, and a rib band a shade darker than the leg (`cuffM`).

**Designs from the shop photos** (all in `data/fixes.json`, each checked against the shop's own page):
- *s5-walk, "dark grey shirt missing the chequer pattern and shows the red version".* The listing page's main image is
  its first colourway, red; the stored photo is now the dark grey colourway's own flat-lay from the same listing (from
  the shop, shrunk as `fetch_photos.py` does, 360 x 450), and a `swatch` of its window-pane check (two repeats cut
  from it, matched to repeat without a seam).
- *h9-boardshort, "flower board short design missing".* Its photo is a lifestyle shot from behind that the page cannot
  read. `swatch`: three flowers cut from the shop's close-up, laid on its blue in a repeating square.
- *s10-admiral, "design on the top isn't clear".* The photo's front was laid on as a flat patch: the side panels showed
  as a faint square. A `place` panel, and two new uses: with `slv` the sleeves stay plain (`placeMap`'s `plainArm`: each
  arm takes the panel's side seam at its height, or the panels ran down his forearms), and `back: false` keeps the back
  plain, as the shop's back photo shows.
- *m7-harrington, "missing the design on this shirt".* The Lambretta polo's band of gold and black checks: `place`, cut
  from the middle of a check square at the centre front so the two mirrored halves meet as one square; `col2` gives its
  tipping gold (it was cream).
- *x11-swim, "print of the t shirt is also missing".* A model photo gives no chest print (by rule: the model may be
  turned). New fields `print` and `at`: the print cut from the shop's flat photo of the tee on a hanger, and where it
  sits as the reader's own prints are placed. The cloth round it is made clear as the reader does (`printCv`); laid on
  the front only (`decal.only`), as the shop's back photo is plain.

**Checks.** `tools/specs.js`: 14 pieces read differently, all meant (the six corrections, and the eight SikSilk pieces
no longer satin). `dump.js` on every outfit, before and after: only the Holiday shirt's reading moved (its new photo).
3D check on the 18 changed outfits and the gate set (46 outfits): clean on his saved shape, slim, athletic, heavier and
loose, and worn tucked in with turn-ups and done up untucked.

## 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzz. The draped scarf wound a turn and a half; draped tops held off a bigger belly (13 Oct 2026)

Emma, 13 Oct: "continue upgrades", in STATUS's order: the draped scarf's knot, its loop behind his neck, g-outdoor-05's
"under", then the draped tops over the heavier belly. All of it **behind the drape switch: with it off (the live page)
nothing changes.** PR #45.

**The scarf template** (`tools/build_garments.py --only scarf`, `data/garments/scarf.json`, 71 KB):
- *The knot, found:* the outer end crossed the front of his throat and then turned straight down flat on his chest. A
  band cannot turn in its own plane without folding on itself, so it bunched where it turned. Wound a turn and a half
  instead ("once round" as it is usually tied: up his front over his right collarbone, round the back, across his
  throat, round the back again and down over his left collarbone), each end leaves the loop at the side of his neck
  and turns down over the curve of his shoulder, which cloth follows without folding. No knot.
- *A narrower band:* 180 x 11 cm (a 22 cm scarf folded once). At 14 cm the turn and a half took so much of it that the
  ends reached only his upper chest (tried 13 Oct, (c) in STATUS); at 11 cm the loop is 1.08 m and the ends 0.66 m
  between them (the longer to the middle of his front).
- *The loop as far out as he is:* an ellipse round his bare neck, measured a little above its base, sat up to 3.5 cm
  inside his shoulders and the jumper's collar at the sides of his neck (his shoulders rise into it there). The loop's
  distance out at each way round his neck is now found by rays from outside at the loop's height, against his body and
  the jumper (`scarf_path`'s `rad`), and the loop is higher at the sides (`side`, 4 cm) than behind.
- *The band's cross-section:* round his neck the half above its middle leans out straight, and the half below bends
  further out as it goes down, by as much as it takes to clear his shoulders and the jumper (found row by row, then
  smoothed along the band; up to 74 degrees at the sides). Leant out straight, its lower edge ran into the slope of his
  shoulders, and moving each point out of him on its own stretched the band there to five or six times its length; the
  cloth takes the shape it is laid in as its own, so it kept those spikes. Laid edge to edge (pattern against draped):
  5% 0.86, 95% 1.29, worst 2.1 (was 0.84, 1.29 and 5.6 at the knot on `main`).
- *Stopped at frame 40 of 90:* by about frame 35 each point moves a millimetre or two in five frames; after that the
  layers' pushing on each other slowly worked the front of the loop up off his throat and crumpled it.
- `SCARF_WRAP` holds the wrap (fwd 0.35, apart 0.055, room 0.018, step 0.01, y 0.012, side 0.04, lean 0.45);
  `GB_SCARF_<NAME>=` tries another without editing.
- *Behind his neck:* the loop's top is where it was (1.547 m; `main` 1.545), but it lies round his neck as a cowl
  instead of standing off it as a flat collar. Lower costs the ends: 1.2 cm lower made the loop 1.22 m and the ends
  0.52 m between them, 2.4 cm lower 1.39 m and 0.34 m (his neck widens fast into his shoulders). Left where it is.

**The page** (switch on):
- *The scarf pushed out over what is under it:* round his neck the rays now also reach behind and at the sides down to
  1.32 m (the loop's lower edge there lies out over his shoulders, and the jacket's back came up over it), and at the
  sides of his neck they come from the side as well as from straight out (an open jacket's collar ends there, its tip
  standing out across the way out from his neck). The points the rays move are then **held** in the short settle after
  it, and the cloth round them follows. g-outdoor-05's "under" (STATUS's item 3 for the scarf, "under 4" on `main` on
  his shape) was found with a probe of the push: the rays did move the scarf 9 mm clear of the draped track jacket's
  collar tip, at the side of his neck where the second end leaves the loop, and the settle then drew those points back
  up to 2 cm. Lowering `make3Dcore`'s stand collar under a draped scarf (STATUS's first suggestion) was tried and did
  nothing: that jacket is draped, its collar the template's. (The check gives the hit in world coordinates; his body,
  and the cloth on it, are in his own, about 2.4% smaller at his height: compare in his.)
- *Draped tops over a bigger belly:* STATUS item 0 read the belly skin as the templates being short. Measured (a probe
  of the settled cloth against his body): at binding no point of the tee is inside him; after the settle 12 points are,
  up to 12 mm deep, all at the height of his trousers' waistband. The layers under a draped top are turned to face away
  from the nearest point of his body (`innerCols`); under the overhang of a bigger belly that point is the belly above
  the waistband and further out, so the waistband faced in and pressed the tee into his belly. They are now turned the
  way his body faces at that point: none inside, on h10-surf and lazy-sunday, and no skin. (Fitting the cloth's length
  to his belly, as STATUS suggested, was tried: it changed nothing on its own, and with the waistband fixed it was not
  needed. Not kept.)

**Checked**, switch on, against `main` with the switch on:
- *The 7 outfits with a draped scarf, on the five bodies:*
  | body | `main`, switch on | this, switch on |
  | --- | --- | --- |
  | his shape | g-outdoor-05 back poke 425, **under 4** | g-outdoor-05 back poke 493 |
  | slim | g-outdoor-05 back poke 66 | g-outdoor-05 back poke 54 |
  | athletic | q7-fairisle belly skin (front 26, side 19); g-outdoor-05 back poke 281 | g-outdoor-05 back poke 323 |
  | heavier | q7-fairisle and q8-morden belly skin (front 186 and 125); g-outdoor-05 back poke 34 | g-outdoor-05 back poke 35 |
  | loose | g-outdoor-05 back poke 598 | g-outdoor-05 back poke 580 |

  The back pokes are the padded shacket (a jacket-weight overshirt `make3Dcore` builds) coming through the draped
  jacket's back, on `main` too; on his shape the patch is a little larger (the waistband rule moved it). It goes when
  jacket-weight overshirts are draped (STATUS item 0.1).
- *The belly set on the heavier body* (h10-surf, jb11-cheapest, lazy-sunday, q7-fairisle, m5-argyle): `main` 5 flagged
  (belly skin 24 to 186 on each, and h10-surf front poke 31), this **0**.
- *The switch-on gate set and STATUS's five more* (31 outfits, his shape): as `main` (m5-argyle front poke 31, the
  shirt's collar over the jumper's neckband, STATUS item 0), but g-outdoor-05 above.
- *Switch off*: the gate set (31 outfits) clean; `tools/specs.js` unchanged; the pull-request check green.

## 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz. Draped padded and puffer jackets (13 Oct 2026)

The next outer layer (STATUS.md item 0.1), behind the drape switch: **with it off (the live page) nothing changes.**
Padded and puffer jackets were the next outer layer by count: 22 outfits wear one (none hooded but o7-ski-jacket),
and every draped top under one was drawn by `make3Dcore` instead.

**The builder** (`tools/build_garments.py --only puffer,puffer_up`, about a minute and a half each in Blender):
- `puffer` (worn open, its front in two) and `puffer_up` (zipped): the track jacket's cut with a padded jacket's room,
  132 cm round the chest (8 more than the track jacket, so it goes over a sweatshirt or a quarter-zip), sleeves 48 cm
  round the bicep, 69 cm long, a 7.5 cm stand collar (the track jacket's is 6.5), a narrow elastic hem (3 cm, gathered
  to 0.92) and 4 cm elastic cuffs.
- `pad`: the padding stiffens every piece, not just the collar. Each piece's bending stiffness is at least `pad`
  (0.15) of the way from plain cloth to the collar's. The `stiff` vertex group now carries each point's own weight
  (it was every stiff point at 1.0, so a `pad` would have made the whole jacket as stiff as its collar); every other
  template's pieces are 0 or 1, so they build as before (not rebuilt).
- Corners where pieces meet +39 degrees at most (the zipped track jacket's +37); bound 22.8 mm off his body at the
  median open, 20.2 mm zipped; 479 and 475 KB.
- What `pad` does is small: built with 0 and with 0.15 the drape is much the same, and the open fronts hang about
  18 cm apart, as the track jacket template's do (`make3Dcore` draws a narrow gap). The quilting is not in the cloth:
  its lines are the material's, as before.

**The page:**
- `drapeArch` draws a padded, puffer, quilted or down jacket from `puffer`, unless it has a hood or is a parka,
  longline, denim, a trucker, Harrington, bomber, leather or suede, a coach, chore or waxed jacket, a fleece or borg,
  a shacket or an overshirt (those keep `make3Dcore`'s shapes). "Button-down collar" is not down.
- `DRAPEOPEN` lists the templates that open (jacket, shirt, puffer: worn open from the template of that name, done up
  from `name_up`); `puffer_up` is a stand collar done up (`STANDC`: a shirt's leaf stays inside it, and a collar
  `make3Dcore` builds under it is the low band, `stC`). The zip up the middle done up, the zip teeth along both edges
  worn open, a small back logo as on the jacket, no photo front (as `make3Dcore`).
- *A layer turned in to hold what is under it (`inCol`) leaves out an open front's edges* (points within 3.5 cm of the
  fronts' centre edge on the pattern, `drapeEdge`). What shows between the edges is not under them: the quarter-zip in
  a padded jacket's opening was pressed in under its edge and into the shirt under it, and the shirt showed through
  (g-quiet-22's front poke).
- *Each point is drawn back to its binding moved out of what is under it* (`drapeOut`, before `drapeSettle`), not to
  the binding itself. The settle's pull home held the padded jacket's open edge where its binding put it, close to his
  body, between the quarter-zip and the shirt (rays through the opening: all three within 4 mm); now the edge is out
  over both (rays through the opening on g-quiet-22: the jacket's edge at 0.247 m, the quarter-zip 0.232, the shirt
  0.219).
  `window.__drapeNoPre` turns it off for comparison. Applied to every draped top: see the checks.

**Checked**, switch on, against `main` switch on:
- *The 22 padded-jacket outfits, his shape:* 21 draped (o7-ski-jacket is hooded). `main` 0 flagged (nothing is draped
  under a padded jacket there); the first try 5 (every one worn open over two layers); now **4**:
  - w20261006-casual-04 (front poke 86) and g-outdoor-16 (front 93), a shirt under a hoodie under the open jacket: the
    shirt's collar showing at the hoodie's neck, beside the hood, and a few flecks of it through the hoodie's lower
    sides, just inside the jacket's open edge near its gathered hem.
  - g-quiet-27 (back poke 42): the tucked shirt `make3Dcore` builds comes about 5 mm through the jacket at the lower
    back, either side (0.95 m).
  - g-quiet-22 (back poke 34): a fleck at the back of an armhole, the armhole flecks item 0 already knows.
  Tried on these and not kept: a thicker push-out (`__drapeTh` 0.016: the front pokes grew) and thicker layers turned
  out under a draped top (`window.__drapeThU` 0.007, from 0.004: g-quiet-27 clean, g-quiet-22's back poke 34 to 90).
  `__drapeThU` stays as a tunable.
- *The gate set, the 22 and ten more draped outfits* (61, his shape): `main` 6 flagged, this 8. The four above are
  new; **g-outdoor-05 (back poke 493: the padded shacket through the draped jacket's back) and q13-coastal (front 41)
  are clean**, and g-outdoor-21's back poke 619 (the borg overshirt through the gilet) is gone, its front poke 150 now
  111: drawing each point back to its binding moved out of what is under it (`drapeOut`) keeps a draped top outside
  a jacket-weight layer `make3Dcore` builds under it, as well as outside the quarter-zip. The rest as `main`
  (m5-argyle front poke 34, errands 50, g-quiet-29 back holes 31).
- *The heavier body* (the 22, g-outdoor-05, g-outdoor-21 and q13-coastal): `main` 2 flagged (g-outdoor-05 back poke 35,
  g-outdoor-21 front 185), this 5: the same four padded-jacket outfits (front poke 103 and 93, back 57 and 46) and
  g-outdoor-21 (front 130); g-outdoor-05 clean.
- *g-outdoor-05 on every body* (`main`, PR #45's table: back poke 35 to 580 on all five): clean on his shape, slim, athletic and
  heavier; back poke 31 on loose. q13-coastal clean on all five.
- *Switch off*: the gate set (31 outfits) clean; `tools/specs.js` unchanged.

## 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz. Short-sleeved "S - S" shirts; a shirt's collar inside a done-up stand collar (14 Oct 2026)

PR #48 (draped clothes only) merged with one 3D check red: w20261006-casual-04 worn done up and untucked
(`--wear zip=up,tuck=out`), front poke 53. A shirt under a SikSilk full-zip hoodie under the Dickies Scobey puffer, zipped
up: the shirt's collar showed at the side of his neck, inside the puffer's 7.5 cm stand collar.

- *The shirt is short-sleeved.* "Stan Ray S - S Flannel Shirt": the shops' feeds write S/S as "S - S" (and others as
  "SS Shirt"), which `guessShape` and `make_outfits.py` did not read, so it was drawn as a long-sleeved shirt, the draped
  `shirt` template, its pink cuffs out of the jacket's sleeves. Both now read `s - s` and `ss` as short sleeves (23 shirts
  in the catalogue, all short-sleeved in their photos); the three outfits that wear the two Stan Ray shirts have them
  as `sshirt`, and `drapeArch` keeps them off the long-sleeved template too.
- *The collar under a stand collar done up.* As an `sshirt` it is `make3Dcore`'s, its collar a 1 cm band under a closed
  hoodie, and that band still showed inside the puffer's collar (front poke 58). Under a draped gilet, zipped jacket or
  zipped puffer (`stC`, whose stand collar is sewn round its neckline) the collar is now only its foot, 4 mm.
  `tools/qa/ray.js` takes `QA_ROT` to probe a pixel the check flagged from its own angle (the front view is 0.15).

**Checked**, his shape, the 71 outfits with a shirt, short-sleeved shirt or polo and a gilet or jacket, as worn and done
up (`--wear zip=up,tuck=out`), against `main`:
- As worn: `main` 11 flagged, this 8. Clean now: g-job-11 (front poke 42), g-job-15 (54) and g-quiet-13 (48), the
  collar inside a gilet's stand collar (STATUS item 0's "8 at the base of his neck"); g-outdoor-21's front poke 70 to 49.
  The rest as `main`: errands, g-quiet-18 and g-outdoor-01 (front poke 44 to 51, the top inside a gilet's collar that is
  not a shirt's), g-quiet-22 (back poke 42), g-mod-22, g-quiet-29 and g-outdoor-06 (back holes 27 to 29).
- Done up: `main` 10 flagged, this 6. Clean now: w20261006-casual-04 (front poke 53, the red check), g-job-11, g-job-15
  and g-quiet-13. The rest as `main`: errands, g-quiet-18, g-outdoor-01, g-outdoor-16 (front poke 44 to 58: a shirt
  under a hoodie under the padded jacket, the hoodie's neck beside the hood, UPGRADE_PLAN's padded-jacket entry),
  g-outdoor-12 and g-quiet-29 (back holes 27 and 30).
- `tools/specs.js`: the two Stan Ray shirts move from `shirt` to `sshirt`; nothing else read differently.

## 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz. Hoods the names do not mention; a hoodie's hood under a hooded jacket (14 Oct 2026)

Before building templates for "the other zip jackets" (STATUS item 0.1), all 143 jackets, coats and gilets worn in
outfits were looked at beside their shop photos. Most of the zip jackets left are hooded or have a collar, so the
track jacket template does not fit them, and 25 of them have a hood the name does not mention ("Montirex Swift
Jacket", "Regatta Northdale insulated work jacket"). They were drawn without one, many as the draped track or puffer
jacket.

- *A `hood` correction* (`data/fixes.json`, true or false, `build_site.py` checks it): `hoodOn` reads it before the
  name, wherever `HOODRE` decided before: the 3D hood (`make3Dcore`), the hood drawn in 2D, a hoodie's hood under it
  (`hoodOut`), and `drapeArch`, which keeps hooded jackets off the track and puffer templates (they are
  `make3Dcore`'s until a hooded template exists). `normFix` passes it through (it dropped any field it did not know).
  25 entries, each checked against its photo. p6-mx-breeze was drawn near black; its photo is slate grey with a
  sage panel, so it gets a colour correction as well.
- *A hoodie's hood under a hooded jacket* now lies inside the jacket's hood, open or closed. Under an open jacket it was
  laid out over the jacket, and the jacket's own hood lay at the same place (g-rave-09 back poke 77, and on `main`
  jb-wet-day, jb8-wet-day and jb9-wet-dealer back poke 85).
- *A jacket's hood under a scarf or neck warmer* starts thin, tucked under it (as under a standing rim), or its top
  lay over the neck warmer at the back of his neck (jb11-winter, under 4).
- *Data:* the Sealskinz Illington is a tee (its photo, and the shop calls it one), filed as a coat; it is now `polo`
  and named as a tee, and g-outdoor-11 (where it was worn as a jacket over a jumper) leaves it out: "Navy jumper and
  stone trousers", 4 pieces.

**Checked**, his shape, the 84 outfits with a jacket that gains a hood, a hoodie under a jacket or coat, or a scarf
under one, plus the gate set, as worn and done up (`--wear zip=up,tuck=out`), against `main`:
- As worn: `main` 8 flagged, this 5. Clean now: jb-wet-day, jb8-wet-day and jb9-wet-dealer (back poke 85). The rest as
  `main`: jb9-ukd-softshell (front poke 53), x11-ellesse (44), jb10-winter-kx3 (55), g-mod-27 (110), st-daily (109).
- Done up: `main` 1 flagged (g-outdoor-16, front poke 58), this 0.
- `tools/specs.js`: the 25 jackets read `fixed: hood`, p6-mx-breeze its new colours, the Sealskinz tee is no longer a
  jacket; nothing else read differently.
- Seen, not fixed: a hoodie's drawstrings fleck the chest under a zipped puffer (the check does not see them);
  dc-3in1-green has no photo.

## 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz. Draped hooded zip jackets and collared zip jackets (14 Oct 2026)

The next of item 0.1's outer layers. Looking at every jacket in an outfit beside its photo (the hood entry above), the
zip jackets the track jacket template did not fit were of two kinds: hooded (shells, windbreakers, softshells, hooded
fleeces) and collared (Harringtons, coach jackets, Capitol and Eisenhower jackets).

- *Four templates* (`tools/build_garments.py`, `MEAS`):
  - `jacket_hood` (worn open) and `jacket_hood_up` (zipped): the track jacket's cut with no collar, a 3 cm hem band,
    and a two-piece hood sewn into the neckline, 37 cm high and 27 deep (a hoodie's is 35 and 25: it goes over a cap).
    The hood is draped after the jacket, as the hoodie's is.
  - `jacket_coll` and `jacket_coll_up`: the track jacket's cut 2 cm shorter, a rib hem, and a shirt's collar a size
    up (a 3 cm stand and a 5 cm leaf, 7.5 cm to its points).
- *In the page:*
  - `drapeArch` gives `jacket_hood` to a jacket with a hood (`hoodOn`), unless it is padded, insulated, a parka, a ski,
    wax, denim or sherpa-lined jacket. These keep `make3Dcore`'s shapes until a hooded puffer exists.
  - It gives `jacket_coll` to a Harrington, coach, Capitol or Eisenhower jacket or a collar blouson (not a padded,
    wax, denim, wool or fleece one, nor a bomber).
  - A stand-collar "zip-up blouson" stays on the track jacket. On the collared template a hoodie under it, zipped,
    showed at the sides of his neck (st-daily, front poke 44); on the track jacket it is clean.
  - The hood is drawn for any template that has one, not only a hoodie's, out over what is worn over it.
  - A hoodie's hood under a hooded jacket, draped or not, is left out (it lies inside the jacket's).
  - A shirt's leaf stays inside any hooded layer, as it did inside a hoodie's hood.
  - Zipped, the hooded jacket gets a zip from its neckline down with a pull at the top. The collared one gets the
    track jacket's zip up to its stand. Worn open, both get zip teeth along each front edge.
  - `jacket_coll_up` counts as a stand collar done up (`STANDC`, `stC`).
- 25 hooded jackets (32 outfits) and 12 collared jackets (17 outfits) are now draped.

**Checked**, his shape, as worn and done up (`--wear zip=up,tuck=out`), against `main`:
- The 32 hooded-jacket outfits: as worn, `main` 0 flagged and this 0. Done up, `main` 0 and this 1: g-quiet-24, back
  holes 29 (limit 25), a sliver of background between his left arm and the zipped jacket's side above the hem. This
  is the kind g-outdoor-12 and g-quiet-29 show on `main`; not fixed.
- The 17 collared-jacket outfits: 0 flagged either way, as on `main`.
- On the other four bodies (slim, athletic, heavier, loose), the 50 outfits as worn, against `main` where flagged:
  - g-outdoor-05 on loose had a back poke of 34: a padded shacket under the hooded jacket came through between his
    shoulder blades. A hooded jacket is now held 7 mm off a jacket-weight overshirt (`thJ`; 4 mm under the other
    templates), and it is clean.
  - Three new flags on athletic, all back holes of the g-quiet-24 kind: g-quiet-24 (52), jb10-offshore (37) and
    g-mod-17 (34). Each is a sliver of background between his left arm, his hand and the jacket's side above the hem.
    Not fixed; next to look at with the other hem holes.
  - The rest are as on `main`: st-daily's front poke on all four (its hoodie under the track jacket, 78 to 100) and
    nw-oldskool's back holes on heavier and loose (35, 30).
- *Also, the small data change STATUS asked for:* g-mod-27's Duck and Cover top is a quarter-zip with no hood in its
  photo (the shop calls it a "1/4 zip hoodie"). It is renamed a quarter-zip sweatshirt, and its piece in g-mod-27 is
  `halfzip` (it was `hoodie`). g-mod-27's front poke of 110 on his shape is gone, and `descOf` reads its zip as half,
  not full.
- `tools/specs.js`: only the Duck and Cover top changes (no longer a hoodie; its zip half).

## 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz. Draped hooded padded jackets (14 Oct 2026)

The next of item 0.1's outer layers: padded and insulated jackets with a hood, which neither the puffer template (a
stand collar) nor `jacket_hood` (a shell's room) fitted.

- *Two templates* (`tools/build_garments.py`, `MEAS`): `puffer_hood` (worn open) and `puffer_hood_up` (zipped), the
  padded jacket's cut and padding with no stand collar and a padded hood, 38 cm high and 28 deep. The neckline is a
  centimetre narrower than the padded jacket's (19 cm). At 20 cm, with no stand collar to hold it, the open jacket's
  padded fronts slid off his shoulders in Blender and the whole jacket fell down his arms.
- *In the page:*
  - `drapeArch` gives `puffer_hood` to a hooded (`hoodOn`) padded, puffer, quilted, down or insulated jacket, unless
    it is a parka, a coat or longline, a ski or 3-in-1 jacket, an overhead smock or denim, wax, leather or sherpa.
  - Zip teeth along each open front, or the zip from the neckline with its pull when done up (as `jacket_hood`).
  - A hooded padded jacket is held 14 mm off the draped layers under it (10 under the others: `layerCols(th)`). At
    10 a lambswool quarter-zip came through its back in spots (w20261008-casual-03, back poke 32).
  - It is held 12 mm off a jacket-weight overshirt under it (`thJ`). At 4 an overshirt's back came through on the
    athletic and loose fits (g-casual-16, 146 and 162); at 7 athletic still had 62.
  - Under a neck warmer it keeps `make3Dcore`'s shapes, its hood tucked under. Draped, the padded hood lay over the
    neck warmer at the back of his neck (jb11-winter, under 3 to 19). Held inside the neck warmer, it bunched and came
    through the jacket's back, whatever the gap.
- Eight jackets in 14 outfits are now draped (the two Closure London puffers, the Brakeburn Landcross, the Hurden, the
  Regatta Northdale, the Passenger Dylan, the Mountain Warehouse Seasons and the Craghoppers Vamos).

**Checked**: the 14 outfits and every outfit with a scarf (21) on all five bodies, as worn and done up: 0 flagged
(`main` 0). Stored specs unchanged.

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
  confirm 1.83 m and the 15.5–16 in neck. (12 Oct 2026: she said to assume the model's current
  shape is right and to make the sizing adjustable, 2zzzzzzzzzzzzzzzzz.)
- A decision on the cropped reference photos. Either a permission rule lets them into the repo,
  or they stay private elsewhere.
- Done 12 Oct 2026: a yes to the newer Three.js and the Blender templates, and proof first behind
  a switch (2zzzzzzzzzzzzzzzzz).
- Which step to start with (recommended: 1 to 3).
