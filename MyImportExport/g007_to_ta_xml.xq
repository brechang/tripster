xquery version "3.0";

(:~
: User: luhkevin
: Date: 11/16/14
: Time: 7:14 PM
: To change this template use File | Settings | File Templates.
:)
declare variable $docname := "export.xml";

declare function local:getUsername($id as xs:integer)
as xs:string?
{
    for $x in doc($docname)/database/USERS/tuple
    where data($x/ID) = $id
    return data($x/USERNAME)
};

declare function local:getAffiliation($id as xs:integer)
as xs:string?
{
    for $x in doc($docname)/database/USERS/tuple
    where data($x/ID) = $id
    return data($x/AFFILIATION)
};

declare function local:getFriends($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/FRIENDS_WITH/tuple
    where data($x/USER_ID) = $id
    return <friend> {local:getUsername(data($x/FRIEND_ID))} </friend>
};

declare function local:getFriendsId($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/FRIENDS_WITH/tuple
    where data($x/USER_ID) = $id
    return <friendid> {local:getUsername(data($x/FRIEND_ID))} </friendid>
};

declare function local:getContentURL($id as xs:integer)
{
    for $x in doc($docname)/database/CONTENT/tuple
    where data($x/ID) = $id
    return data($x/URL)
};

declare function local:getContent($id as xs:integer)
as element()*
{
   for $x in doc($docname)/database/CONTENT_OF/tuple
   where data($x/ALBUM_ID) = $id
   return
   <content>
        <id> {data($x/CONTENT_ID)} </id>
        <group> group1 </group>
        <type> photo </type>
        <url> {local:getContentURL($x/CONTENT_ID)}</url>
   </content>
};

declare function local:getAlbumName($id as xs:integer)
as xs:string
{
    for $x in doc($docname)/database/ALBUM/tuple
    where data($x/ID) = $id
    return data($x/NAME)
};

declare function local:getAlbum($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/ALBUM_OF/tuple
    where data($x/TRIP_ID) = $id
    return
        <album>
            <id> {data($x/ALBUM_ID)} </id>
            <name> {local:getAlbumName(data($x/ALBUM_ID))} </name>
            <privacyFlag> private </privacyFlag>
            {local:getContent(data($x/ALBUM_ID))}
        </album>
};

declare function local:getLocationName($id)
as xs:string
{
    for $x in doc($docname)/database/LOCATION/tuple
    where data($x/ID) = $id
    return data($x/NAME)
};

declare function local:getLocation($id)
as element()*
{
    for $x in doc($docname)/database/TRIP/tuple
    where data($x/USER_ID) = $id
    return <location> {local:getLocationName(data($x/LOCATION_ID))} </location>
};

declare function local:getTrip($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/PARTICIPANTS_OF/tuple
    where data($x/USER_ID) = $id
    return
        <trip>
            <id> {data($x/TRIP_ID)} </id>
            <name> foo name </name>
            <feature> foo feature </feature>
            <privacyFlag> private </privacyFlag>
            {local:getAlbum($x/TRIP_ID)}
            {local:getLocation($x/TRIP_ID)}
        </trip>
};

declare function local:getUserTripRating($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/PARTICIPANTS_OF/tuple
    where data($x/USER_ID) = $id
    return
        <rateTrip>
            <id> {data($x/TRIP_ID)} </id>
            {local:getTripScore($x/TRIP_ID)}
            {local:getTripComments($x/TRIP_ID)}
        </rateTrip>
};

declare function local:getTripComments($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/TRIP_COMMENTS/tuple
    where data($x/TRIP_ID) = $id
    return <comments>{data($x/COMMENT_STR)}</comments>
};

declare function local:getTripScore($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/TRIP/tuple
    where data($x/ID) = $id
    return
        <score>{data($x/RATING)}</score>
};

declare function local:getUserTripID($id as xs:integer)
as xs:integer
{
    for $x in doc($docname)/database/PARTICIPANTS_OF/tuple
    where data($x/USER_ID) = $id
    return data($x/TRIP_ID)
};

declare function local:getUserTripAlbum($id as xs:integer)
as xs:integer
{
  for $x in doc($docname)/database/ALBUM_OF/tuple
  where data($x/TRIP_ID) = $id
  return data($x/ALBUM_ID)
};

declare function local:getUserAlbumContent($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/CONTENT_OF/tuple
    where data($x/ALBUM_ID) = $id
    return $x
};

declare function local:getUserContentRating($id as xs:integer)
as element()*
{
    for $x in local:getUserAlbumContent(local:getUserTripAlbum(local:getUserTripID($id)))
        (: doc($docname)/database/CONTENT/tuple :)
    (: where data($x/ID) = local:getUserAlbumContent(local:getUserTripAlbum(local:getUserTripID($id))) :)

    return
        <rateContent>
            <contentid>{data($x/CONTENT_ID)}</contentid>
            <contentSource>group1</contentSource>
            <score>{data($x/RATING)}</score>
            {local:getContentComment(data($x/CONTENT_ID))}
        </rateContent>
};

declare function local:getContentComment($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/CONTENT_COMMENTS/tuple
    where data($x/CONTENT_ID) = $id
    return
        <comment>{data($x/COMMENT_STR)}</comment>

};

declare function local:getTripsterData() as
element()*
{
for $x in doc($docname)/database/USERS/tuple/ID
return
<User>
    <login> {local:getUsername($x)} </login>
    <email> {local:getUsername($x)}@example.com </email>
    <name> {local:getUsername($x)} </name>
    <affiliation> {local:getAffiliation($x)} </affiliation>
    <interests> Surfing </interests>
    {local:getFriends($x)}
    {local:getTrip($x)}
    {local:getUserTripRating($x)}
    {local:getUserContentRating($x)}

    <request>
        <tripid> 3 </tripid>
        <status> pending </status>
    </request>

    <invite>
        <tripid> 1 </tripid>
        {local:getFriendsId($x)}
        <status> pending </status>
    </invite>
</User>
};

<tripster xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ta_tripster.xsd">
    {local:getTripsterData()}
</tripster>
