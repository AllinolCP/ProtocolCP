from cmd import Cmd

class MyPrompt(Cmd):

    #-----------#
    # Blackhole #
    #-----------#

    def do_blackhole(self, args):
        print('''
            %xt%jnbhg%{$this->internalId}%{$this->externalId}%
            %xt%lnbhg%{$penguin->room->internalId}%{$penguin->room->externalId}%
            %xt%jg%{$this->internalId}%{$this->externalId}%
            ''')

    #-----#
    # EPF #
    #-----#

    def do_epf(self, args):
        print('''
            ***Handlers***
            f#epfga => handleGetAgentStatus
            f#epfsa => handleSetAgentStatus
            f#epfgr => handleGetAgentPoints
            f#epfai => handleAddAgentItem
            f#epfgm => handleGetComMessages
            f#epfgf => handleEPFGF
            ***Packets***
            %xt%epfga%-1%{$penguin->EPF['status']}%
            %xt%epfsa%-1%1%
            %xt%epfgr%-1%{$penguin->EPF['career']}%{$penguin->EPF['points']}%
            %xt%epfai%-1%{$penguin->EPF['points']}%
            %xt%epfgm%-1%0%
            %xt%zr%{$penguin->room->internalId}%" . rand(1, 10) . "," . rand(1, 10) . "," . rand(1, 10) . "%" . rand(1, 5) . "%"
            %xt%zc%{$penguin->room->internalId}%%0%0%0%
            %xt%epfgf%-1%1%
            ''')

    #-------#
    # Party #
    #-------#

    def do_party(self, args):
        print('''
            ***Handlers***
            frozen#partycookie => handlePartyCookie
            party#partycookie => handlePartyCookie
            frozen#fpmsgviewed => handleFrozenMessage
            frozen#fpupdateroomstate => handleUpdateRoomState
            frozen#fpactivatefreezingpower => handleActivateFreezing
            frozen#fpfindsnowflake => handleFindSnowflake
            frozen#fptransform => handleTransform
            frozen#fpfurniturepack => FrozenAddInventory
            ***Packets***
            frozen#partycookie: %xt%partycookie%-1%{"msgViewedArray":['.$partymsg.'],"snowflakes":['. $snowflakes .'],"freezingPowers":'.$freezingPower.',"login":0}%'
            party#partycookie: %xt%partycookie%-1%{"msgViewedArray":['. $partymsg .'],"communicatorMsgArray":['. $partycmq .'],"questTaskStatus":['. $partyquest .']}%'
            frozen#fpupdateroomstate: %xt%fpupdateroomstate%-1%{$penguin->id}%$part%$type%$x%$y%
            frozen#fpfurniturepack: %xt%fpfurniturepack%-1%0%
            The other handlers had no packets assigned to them.
            ''')

    #-----------#
    # Star Wars #
    #-----------#

    def do_starwars(self, args):
        print('''
            Run the command: starwarshandler for the battle handler.
            %xt%partycookie%-1%{"msgViewedArray":[' . $party['msgviewed'] . '],"qcMessageArray":[' . $party['qc'] . '],"questTaskStatus":[' . $party['tasks'] . '],"points":' . $party['points'] . '}%
            %xt%swopen%{$penguin->room->internalId}%{$penguin->id}%
            %xt%swclose%{$penguin->room->internalId}%{$penguin->id}%
            $battleId = rand(1, 5000);
            echo "\n[DUEL]: id1:{$id}, id2:{$id2}, battleId:{$battleId}\n";
            %xt%swjoin%2%138393484%223277305%5000%47%
            %xt%swjoin%' . $penguin->room->internalId . '%' . $battlePlayer1 . '%' . $battlePlayer2 . '%5000%' . $battleId . '%'
            %xt%swresult%{$penguin->room->internalId}%
            ''')

    def do_starwarshandler(self, args):
        print('''
        echo "1\n";
        $penguin->chosenMove = Packet::$Data[2];
        echo "2\n";
        $battleId = Packet::$Data[3];
        echo "3\n";
        $move = Packet::$Data[2];
        echo "4\n";
        $battle = $penguin->database->getBattleInfo($battleId);
        echo "5\n";
        $battle = explode(',', $battle);
        echo "6\n";
        $battlePlayer1 = $battle[0];
        echo "7\n";
        $battlePlayer2 = $battle[1];
        echo "8\n";
        if($penguin->id == $battlePlayer1) {
        echo "9\n";
            $player1 = 'me';
            echo "10\n";
        } else {
        echo "11\n";
            $player1 = 'him';
            echo "12\n";
        }
        if($player1 == 'me') {
        echo "13\n";
            foreach($this->penguins as $p2) {
            echo "14\n";
                if($p2->id == $battlePlayer2) {
                echo "15\n";
                    $mymove = $move;
                    echo "16\n";
                    $hismove = $p2->chosenMove;
                    echo "17\n";
                    switch($mymove) {
                        case 0:
                            if($hismove == 0) {
                                $this->handleResult($battleId,$sock, $battlePlayer1, $battlePlayer2, 'tie', 0, 0);
                            } 
                            if($hismove == 1) {
                                $this->handleResult($battleId,$sock, $battlePlayer1, $battlePlayer2, 'lost', 0, 1);
                            }
                            if($hismove == 2) {
                                $this->handleResult($battleId,$sock, $batttlePlayer1, $battlePlayer2, 'won', 0, 2);
                            }
                        break;
                        case 1:
                            if($hismove == 1) {
                                $this->handleResult($battleId,$sock, $battlePlayer1, $battlePlayer2, 'tie', 1, 1);
                            } 
                            if($hismove == 2) {
                                $this->handleResult($battleId,$sock, $battlePlayer1, $battlePlayer2, 'lost', 1, 2);
                            }
                            if($hismove == 0) {
                                $this->handleResult($battleId,$sock, $batttlePlayer1, $battlePlayer2, 'won', 1, 0);
                            }
                        break;
                        case 2:
                            if($hismove == 0) {
                                $this->handleResult($battleId,$sock, $battlePlayer1, $battlePlayer2, 'lost', 2, 0);
                            } 
                            if($hismove == 1) {
                                $this->handleResult($battleId,$sock, $battlePlayer1, $battlePlayer2, 'win', 2, 1);
                            }
                            if($hismove == 2) {
                                $this->handleResult($battleId, $sock, $batttlePlayer1, $battlePlayer2, 'tie', 2, 2);
                            }
                        break;
                    }
                    echo "18\n";
                    $party['tasks'] = $p2->questtasks;
                    $party['msgviewed'] = $p2->msgviewed;
                    $party['points'] = $p2->sw_points;
                    $party['qc'] = $p2->qc_msg;
                    $p2->send('%xt%partycookie%-1%{"msgViewedArray":[' . $party['msgviewed'] . '],"qcMessageArray":[' . $party['qc'] . '],"questTaskStatus":[' . $party['tasks'] . '],"points":' . $party['points'] . '}%');
            ''')

    #------------#
    # Navigation #
    #------------#

    def do_navigation(self, args):
        print('''
            ***Handlers***
            j#js => HandleJoinWorld
            j#jr => handleJoinRoom
            j#jg => handleJoinGame
            j#jp => handleJoinPlayerRoom
            ***Packets***
            j#js: %xt%js%-1%1%{$penguin->EPF['status']}%$isModerator%1%
            j#jr: 101|Jadbalout|45|4|0|0|0|0|0|0|0|0|0|0|1|1|0|0|{"spriteScale":100,"spriteSpeed":100,"ignoresBlockLayer":false,"invisible":false,"floating":false}
            j#jg: %xt%jg%-1%intRoom%
            j#jp: %xt%jp%$playerId%$playerId%$externalId%$roomType%
            j#grs: %xt%grs%-1%{$this->externalId}%{$this->getRoomString()}%
            ''')

    #-----------#
    # Transform #
    #-----------#

    def do_transform(self, args):
        print('''
            ***Handlers***
            pt#spts => handleAvatarTransformation
            ***Packets***
            pt#spts: %xt%spts%{$penguin->room->internalId}%{$penguin->id}%$avatarId%
            $avatarId: {"spriteScale":100,"spriteSpeed":100,"ignoresBlockLayer":false,"invisible":false,"floating":false}
            ''')

    #--------------#
    # Games/Waddle #
    #--------------#

    def do_games(self, args):
        print('''
            The handlers should be wrapped in the following: "z" => array(//Handlers)
            ***Handlers***
            zo => handleGameOver
            gz => handleGetGame
            m => handleGameMove
            gw => handleGetWaddlesPopulationById
            jw => handleSendJoinWaddleById
            lw => handleLeaveWaddle
            jz => handleStartGame
            lz => handleQuitGame
            zm => handleSendMove
            ***Packets***
            ''')
        
    #---------#
    # Buddies #
    #---------#
    
    def do_buddies(self, args):
        print('''
            ***Handlers***
            b#ba => handleBuddyAccept
            b#bf => handleBuddyFind
            b#br => handleBuddyRequest
            b#gb => handleGetBuddies
            b#rb => handleBuddyRemove
            b#bon => handleBuddyOnline
            b#bof => handleBuddyOffline
            u#gbffl => handleGetBestFriendsList
            u#pbsu => handlePlayerBySwidUsername
            ***Packets***
            b#ba: %xt%ba%$objClient->getIntRoom()%$intPlayer%$strUsername%
            b#bf: %xt%bf%$objClient->getIntRoom()%$intRoom%
            b#br: %xt%br%$objClient->getIntRoom()%$objClient->getPlayer()%$objClient->getUsername()%
            b#gb: %xt%gb%-1%$strBuddies%
            [IF BUDDY ONLINE] b#rb: %xt%rb%$objClient->getIntRoom()%$objClient->getPlayer()%$objClient->getUsername()%
            [IF BUDDY OFFLINE] b#rb: %xt%rb%$objClient->getIntRoom()%$intTarget%$this->objDatabase->getUsername($intTarget)%
            b#bon: %xt%bon%0%123%
            b#bof: %xt%bof%0%123%
            u#gbffl: %xt%gbffl%{$penguin->room->internalId}%
            u#pbsu: %xt%pbsu%{$penguin->room->internalId}%$usernameList%
            ''')

    #--------#
    # Tracks #
    #--------#

    def do_tracks(self, args):
        print('''
            ***Handlers***
            musictrack#broadcastingmusictracks => handleBroadcastingTracks
            musictrack#getsharedmusictracks => handleGetSharedMusicTracks
            musictrack#getmymusictracks => handleGetMyMusicTracks
            musictrack#savemymusictrack => handleSaveMyMusicTrack
            musictrack#refreshmytracklikes => handleRefreshMyTrackLikes
            musictrack#loadmusictrack => handleLoadMusicTrack
            musictrack#sharemymusictrack => handleShareMyMusicTrack
            musictrack#deletetrack => handleDeleteMusicTrack
            musictrack#canliketrack => handleCanLikeMusicTrack
            musictrack#liketrack => handleLikeMusicTrack
            ***Packets***
            musictrack#broadcastingmusictracks: %xt%broadcastingmusictracks%-1%$sharedTracksCount%$playlistPosition%$sharedPlayerTracks%
            musictrack#broadcastingmusictracks: %xt%broadcastingmusictracks%-1%$sharedTracksCount%$playlistPosition%$sharedPlayerTracks%
            musictrack#broadcastingmusictracks: %xt%broadcastingmusictracks%-1%0%-1%%
            musictrack#getsharedmusictracks: %xt%getsharedmusictracks%-1%$sharedTracksCount%$sharedTracksData%
            musictrack#getsharedmusictracks: %xt%getsharedmusictracks%-1%0%%
            musictrack#getmymusictracks: %xt%getmymusictracks%-1%0%%
            musictrack#getmymusictracks: %xt%getmymusictracks%-1%$trackCount%$musicTracks%
            musictrack#savemymusictrack: %xt%savemymusictrack%-1%$trackId%
            musictrack#refreshmytracklikes: %xt%getlikecountfortrack%-1%{$penguin->id}%$trackId%$trackLikes%
            musictrack#loadmusictrack: %xt%loadmusictrack%-1%$trackData%
            musictrack#sharemymusictrack: %xt%sharemymusictrack%-1%1%
            musictrack#deletetrack: %xt%deletetrack%-1%1%
            musictrack#canliketrack: %xt%canliketrack%-1%$trackId%1%
            musictrack#canliketrack: %xt%canliketrack%-1%$trackId%0%
            musictrack#canliketrack: %xt%canliketrack%-1%$trackId%1%
            musictrack#liketrack: %xt%liketrack%6%$ownerId%$trackId%$likeCount%
            ''')

    #------#
    # Toys #
    #------#

    def do_toys(self, args):
        print('''
            ***Handlers***
            t#at => handleOpenPlayerBook
            t#rt => handleClosePlayerBook
            ***Packets***
            t#rt: %xt%rt%{$penguin->room->internalId}%{$penguin->id}%
            t#at: %xt%at%{$penguin->room->internalId}%{$penguin->id}%$toyId%1%
            ''')

    #------------#
    # Redemption #
    #------------#
    
    def do_redemption(self, args):
        print('''
            'The handlers should be wrapped in the following: "red" => array(//Handlers)'
            ***Handlers***
            rjs => handleJoinRedemption
            rsc => handleSendCode
            ***Packets***
            rjs: %xt%rjs%-1%%1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17%0%
            rsc: %xt%rsc%-1%{$type}%{$items}%{$redemptionCoins}%
            ''')
    
    #--------#
    # Errors #
    #--------#
    
    def do_errors(self, args):
        print "Example: %xt%e%0%100%"
        print('''
            1: Connection Lost
            2: Time Out
            3: Multiple Connections
            4: Disconnect
            5: Kick
            6: Connection Not Allowed
            100: Username Not Found
            101: Incorrect Password
            103: Server Full
            104: Old Salt Error
            130: Password Required
            131: Password Short
            132: Password Long
            140: Name Required
            141: Name Short
            142: Name Long
            150: Login Flooding
            200: Player In Room
            210: Room Full
            211: Game Full
            212: Room Capacity Rule
            213: Room Does Not Exist
            400: Already Owns Inventory Item
            401: Not Enough Coins
            402: Item Does Not Exist
            403: Max Furniture Items
            405: Not Enough Medals
            406: Max pufflecare items
            407: Max Puffle Hat Items
            408: Already Owns Superplay Item
            409: Max Card-Jitsu Mats
            410: Item Not Available
            440: Puffle Limit
            441: Name Not Available
            442: Puffle Limit
            500: Already Owns Igloo
            501: Already Owns Floor
            502: Already Owns Location
            601: Ban Duration
            602: Ban An hour
            603: Ban Forever
            610: Autoban
            611: Hacking Autoban
            800: Game Cheat
            851: Invalid room id specified in j#jr
            900: Account Not Activated
            901: Buddy Limit
            910: Play Time Up
            911: Out Play Time
            913: Grounded
            914: Play Time Ending
            915: Play Hours Ending
            916: Play Hours Up
            917: Play Hours Hasn't Started
            918: Play Hours Up
            990: System Reboot
            999: Not A Member
            1000: No Database Connection
            10001: No Socket Connection
            10002: Timeout
            10003: Password Save Prompt
            10004: Socket Lost Connection
            10005: Load Error
            10006: Max Igloo Furniture Error
            10007: Multiple Connections
            10008: Connection Timeout
            10009: Max Stampbook Cover Items
            10010: Web Service Load Error
            10011: Web Service Send Error
            10104: Chrome Mac Login Error
            20001: Redemption Connection Lost
            20002: Redemption Already Have Item
            20103: Redemption Server Full
            20140: Name Required Redemption
            20130: Password Required Redemption
            20131: Password Short Redemption
            20710: Redemption Book ID Not Exist
            20711: Redemption Book Already Redemeed
            20712: Redemption Book Wrong Answer
            20713: Redemption Book Too Many Attempts
            20720: Redemption Code Not Found
            20721: Redemption Code Already Redeemed
            20722: Redemption Too Many Attempts
            20723: Redemption Catalog Not Found
            20724: Redemption No Exclusive Redeems
            20725: Redemption Code Group Redeemed
            20726: Redemption Code Expired
            20730: Redemption Puffles Max
            21700: Redemption Invalid Puffle
            21701: Redemption Puffle Code Max
            21702: Redemption Code Too Short
            21703: Redemption Code Too Long
            21704: Golden Code Not Ready
            21705: Redemption Puffle Name Empty
            ''')

    #-----#
    # XML #
    #-----#

    def do_xml(self, args):
        print('''
            <msg t="sys"><body action="apiOK" r="0"></body></msg>
            <msg t='sys'><body action='verChk' r='0'><ver v='153' /></body></msg>
            <msg t="sys"><body action="rndK" r="-1"><k>randomkey</k></body></msg>
            <policy-file-request/>
            <cross-domain-policy><allow-access-from domain="*.domain.com" to-ports="*" /></cross-domain-policy>
            <msg t='sys'><body action='login' r='0'><login z='w1'>
	        <nick><![CDATA[" Username "]]></nick>
		    <pword><![CDATA[" Hashed Password "]]></pword>
		    </login></body></msg>
            ''')

    #-----------#
    # Inventory #
    #-----------#

    def do_inventory(self, args)
    print('''
    	***Handlers***
    	i#gi => handleGetInventory
    	i#ai => handleBuyInventory
    	st#sse => handleStampAdd
		st#gps => handleGetStamps
		st#gmres => handleGetRecentStamps
		st#gsbcd => handleGetBookCover
		st#ssbcd => handleUpdateBookCover
    	***Packets***
    	i#gi: %xt%gi%-1%$inventoryList%
    	i#ai: %xt%ai%{$this->room->internalId}%$itemId%{$this->coins}%
    	''')

    #-------------------------#
    # Stamps, Pins and Awards #
    #-------------------------#

    def do_stamps(self, args):
    	print('''
    		***Handlers***
    		i#qpp => handleGetPlayerPins
    		i#qpa => handleGetPlayerAwards
    		***Packets***
    		i#qpp: %xt%qpp%-1%$pins%
    		i#qpa: %xt%qpa%-1%$playerId%%

    		''')


    #---------#
    # Helpers #
    #---------#

    def do_quit(self, args):
        print "Quitting."
        raise SystemExit

    def do_Quit(self, args):
        print "Quitting."
        raise SystemExit

    def do_exit(self, args):
        print "Quitting."
        raise SystemExit

    def do_Exit(self, args):
        print "Quitting."
        raise SystemExit

    def do_info(self, args):
        print('''
            ProtocolCP is an open-source, easy to use and free tool for CPPS Developers.
            You will find almost every handler (AS2 & AS3) for Club Penguin.
            The reason I created this is because a lot of users don't even know the packet-side of Club Penguin.
            Discord: Zaseth#7550
            ''')

    #----------#
    # FindFour #
    #----------#

    def do_findfour(self, args):
        print(
            '''
            [RECIEVE] Data [%xt%z%gz%-1%] incoming from 
            [SENT] Sent [ %xt%gz%-1%P2%P1%0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,% ] to 
            [RECIEVE] Data [%xt%z%jz%-1%] incoming from 
            [SENT] Sent [ %xt%uz%-1%1%P1% ] to 
            [SENT] Sent [ %xt%uz%-1%0%P2% ] to 
            [SENT] Sent [ %xt%uz%-1%1%P1% ] to 
            [SENT] Sent [ %xt%jz%-1%1%1% ] to 
            [SENT] Sent [ %xt%sz%-1% ] to 
            [SENT] Sent [ %xt%sz%-1% ] to 
            [RECIEVE] Data [%xt%s%u#sf%-1%22%] incoming from 
            [SENT] Sent [ %xt%sf%-1%1%22% ] to 
            [SENT] Sent [ %xt%sf%-1%1%22% ] to 
            [RECIEVE] Data [%xt%z%zm%-1%6%5%] incoming from 
            [SENT] Sent [ %xt%zm%-1%0%6%5% ] to 
            [SENT] Sent [ %xt%zm%-1%0%6%5% ] to 
            [RECIEVE] Data [%xt%s%u#h%-1%] incoming from 
            [SENT] Sent [ %xt%h%-1% ] to 
            [RECIEVE] Data [%xt%z%zm%-1%5%5%] incoming from 
            [SENT] Sent [ %xt%zm%-1%1%5%5% ] to 
            [SENT] Sent [ %xt%zm%-1%1%5%5% ] to 
            [RECIEVE] Data [%xt%z%zm%-1%6%4%] incoming from 
            [SENT] Sent [ %xt%zm%-1%0%6%4% ] to 
            [SENT] Sent [ %xt%zm%-1%0%6%4% ] to 
            [RECIEVE] Data [%xt%z%zm%-1%5%4%] incoming from 
            [SENT] Sent [ %xt%zm%-1%1%5%4% ] to 
            [SENT] Sent [ %xt%zm%-1%1%5%4% ] to 
            [RECIEVE] Data [%xt%z%zm%-1%6%3%] incoming from 
            [SENT] Sent [ %xt%zm%-1%0%6%3% ] to 
            [SENT] Sent [ %xt%zm%-1%0%6%3% ] to 
            [RECIEVE] Data [%xt%z%zm%-1%5%3%] incoming from 
            [SENT] Sent [ %xt%zm%-1%1%5%3% ] to 
            [SENT] Sent [ %xt%zm%-1%1%5%3% ] to 
            [RECIEVE] Data [%xt%z%zm%-1%6%2%] incoming from 
            [SENT] Sent [ %xt%zm%-1%0%6%2% ] to 
            [SENT] Sent [ %xt%zm%-1%0%6%2% ] to 
            [SENT] Sent [ %xt%zo%-1%167% ] to 
            [SENT] Sent [ %xt%zo%-1%221% ] to 
            [RECIEVE] Data [%xt%s%a#lt%-1%] incoming from 
            [RECIEVE] Data [%xt%s%a#lt%-1%] incoming from
            ''')

    #------------#
    # Card-Jitsu #
    #------------#

    def do_glitch(self, args):
        print(
            '''
            00:22:19.764 - [ INFO ] > { DATA OUT } : %xt%jz%138%1%Lake%1%3%
            00:22:19.764 - [ INFO ] > { DATA OUT } : %xt%uz%138%0|Sensei|14|0%1|Lake|1|3%
            00:22:19.765 - [ INFO ] > { DATA OUT } : %xt%sz%138%
            00:22:23.839 - [ INFO ] > { DATA IN } : %xt%z%zm%138%deal%5%
            00:22:23.840 - [ INFO ] > { DATA OUT } : %xt%zm%138%deal%1%31|17|s|2|r|0%32|22|w|5|b|0%33|51|f|6|b|0%34|9|f|2|y|0%35|26|w|4|p|0%
            00:22:23.840 - [ INFO ] > { DATA OUT } : %xt%zm%138%deal%0%0|747|w|11|p|7%1|543|f|3|p|0%2|710|s|3|p|0%3|352|f|12|o|9%4|634|w|3|g|0%
            00:22:26.254 - [ INFO ] > { DATA IN } : %xt%z%zm%138%pick%32%
            aaaaa1
            aaaaa1
            352|22|false|1
            aa1
            00:22:26.255 - [ INFO ] > { DATA OUT } : %xt%zm%138%pick%1%32%
            00:22:26.256 - [ INFO ] > { DATA OUT } : %xt%zm%138%pick%0%0%
            00:22:26.257 - [ INFO ] > { DATA OUT } : %xt%zm%138%judge%0%-1%
            ''')

    def do_corrupt(self, args):
        print(
            '''
            00:06:08.326 - [ INFO ] > { DATA IN } : %xt%s%j#jr%16%951%0%0%
            00:06:08.343 - [ INFO ] > { DATA OUT } : %xt%jg%121%951%
            00:06:09.153 - [ INFO ] > { DATA IN } : %xt%z%jsen%121%
            00:06:09.153 - [ INFO ] > { DATA OUT } : %xt%scard%121%998%77797016%2%
            00:06:09.424 - [ INFO ] > { DATA IN } : %xt%s%w#jx%121%998%77797016%2%
            00:06:09.424 - [ INFO ] > { DATA OUT } : %xt%jx%138%998%
            00:06:09.672 - [ INFO ] > { DATA IN } : %xt%z%gz%138%3%
            00:06:09.672 - [ INFO ] > { DATA OUT } : %xt%gz%138%2%1%
            00:06:09.690 - [ INFO ] > { DATA IN } : %xt%z%jz%138%
            00:06:09.690 - [ INFO ] > { DATA OUT } : %xt%jz%138%1%Lake%1%10%
            00:06:09.691 - [ INFO ] > { DATA OUT } : %xt%uz%138%0|Sensei|14|0%1|Lake|1|10%
            00:06:09.691 - [ INFO ] > { DATA OUT } : %xt%sz%138%
            00:06:13.227 - [ INFO ] > { DATA IN } : %xt%z%zm%138%deal%5%
            00:06:13.228 - [ INFO ] > { DATA OUT } : %xt%zm%138%deal%1%31|9|f|2|y|0%32|20|s|7|y|0%33|73|f|10|y|1%34|112|w|4|p|0%35|72|f|9|b|16%
            00:06:13.229 - [ INFO ] > { DATA OUT } : %xt%zm%138%deal%0%0|96|f|11|r|4%1|563|f|5|g|0%2|237|w|7|b|0%3|633|w|2|g|0%4|540|w|8|b|0%
            00:06:14.275 - [ INFO ] > { DATA IN } : %xt%z%zm%138%pick%34%
            00:06:14.276 - [ INFO ] > { DATA OUT } : %xt%zm%138%pick%1%34%
            aa1
            aa1
            aa1
            aa1
            aaaaa1
            00:06:14.277 - [ INFO ] > { DATA OUT } : %xt%zm%138%pick%0%1%
            00:06:14.277 - [ INFO ] > { DATA OUT } : %xt%zm%138%judge%1%-1%
            00:07:02.639 - [ INFO ] > { DATA IN } : %xt%s%j#jr%16%951%0%0%
            00:07:02.661 - [ INFO ] > { DATA OUT } : %xt%jg%121%951%
            00:07:05.166 - [ INFO ] > { DATA IN } : %xt%z%jsen%121%
            00:07:05.167 - [ INFO ] > { DATA OUT } : %xt%scard%121%998%4686175%2%
            00:07:05.457 - [ INFO ] > { DATA IN } : %xt%s%w#jx%121%998%4686175%2%
            00:07:05.457 - [ INFO ] > { DATA OUT } : %xt%jx%138%998%
            00:07:05.771 - [ INFO ] > { DATA IN } : %xt%z%gz%138%3%
            00:07:05.771 - [ INFO ] > { DATA OUT } : %xt%gz%138%2%1%
            00:07:05.786 - [ INFO ] > { DATA IN } : %xt%z%jz%138%
            00:07:05.786 - [ INFO ] > { DATA OUT } : %xt%jz%138%1%Lake%1%3%
            00:07:05.786 - [ INFO ] > { DATA OUT } : %xt%uz%138%0|Sensei|14|0%1|Lake|1|3%
            00:07:05.786 - [ INFO ] > { DATA OUT } : %xt%sz%138%
            00:07:09.287 - [ INFO ] > { DATA IN } : %xt%z%zm%138%deal%5%
            00:07:09.288 - [ INFO ] > { DATA OUT } : %xt%zm%138%deal%1%31|1|f|3|b|0%32|43|s|5|r|0%33|26|w|4|p|0%34|60|s|8|o|0%35|23|w|2|g|0%
            00:07:09.288 - [ INFO ] > { DATA OUT } : %xt%zm%138%deal%0%0|30|w|2|y|0%1|403|s|4|p|0%2|81|s|10|g|1%3|605|f|6|r|0%4|587|f|12|r|11%
            00:07:10.304 - [ INFO ] > { DATA IN } : %xt%z%zm%138%pick%33%
            00:07:10.305 - [ INFO ] > { DATA OUT } : %xt%zm%138%pick%1%33%
            aaaa1
            aaaa1
            30|26|false|1
            aaaaa1
            00:07:10.305 - [ INFO ] > { DATA OUT } : %xt%zm%138%power%0%1%1%
            00:07:10.305 - [ INFO ] > { DATA OUT } : %xt%zm%138%judge%0%-1%
            0
            ''')

    def do_cjwaddle(self, args):
        print '%xt%tmm%0%-1%" . $client->username . "%" . $player->username . "%"'
        print "%xt%scard%0%998%{$matchid}%2%"
        print '%xt%tmm%0%-1%" . $player->username . "%" . $client->username . "%"'
        print "%xt%scard%0%998%{$matchid}%2%"
        print '%xt%tmm%0%-1%" . $client->username . "%Sensei%"'
        print "%xt%scard%0%998%{$matchid}%1%"
        print "%xt%zm%{$client->matchID}%power%0%1%"
        print "%xt%zm%{$client->matchID}%power%0%1%"
        print "%xt%zm%{$client->matchID}%judge%0%-1%"

    def do_cjinfo(self, args):
        print(
            '''
            if($cmd == "gz") // Message get game
            // %xt%gz% max Players Packet % number of players Packet %
            $user->sendPacket("%xt%gz%0%0%");
            if($cmd == "jz") // Message join game
            // %xt%jz% seatID % Nickname % Color % Rank %
            $user->sendPacket("%xt%jz%0%" . $user->username . "%" . $user->colour . "%0%");
            if($cmd == "uz") // Message update game
            // %xt%uz% players packet %
            $user->sendPacket("%xt%uz%%");
            if($cmd == "sz") // Message start game
            // %xt%sz% data message (wtf?) %
            $user->sendPacket("%xt%sz%%");
            if($cmd == "zm") // Message game move
            // %xt%zm% instr packet (WTF!!!) % data message (wtf?) %
            $user->sendPacket("%xt%zm%%%");
            if($cmd == "cz") // Message close game
            // %xt%cz% nickname %
            $user->sendPacket("%xt%cz%" . $user->username . "%");
            if($cmd == "lz") // Message leave game
            // %xt%lz% seatID %
            $user->sendPacket("%xt%lz%0%");
            if($cmd == "czo") // Message game over
            // %xt%czo% coins % winseat % ids %
            $user->sendPacket("%xt%czo%0%0%%");
            if($cmd == "cza") // Message game award
            // %xt%cza% rank %
            $user->sendPacket("%xt%cza%%");
            if($cmd == "cjsi") // Message stamp info
            // %xt%cjsi% stamp info %
            $user->sendPacket("%xt%cjsi%0%");
            ''')

    def do_fire0(self, args):
        print "Card-Jitsu Fire SEAT ID 0"
        print(
            '''
            01:46:40.091 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:46:40.091 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:46:41.328 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%4%
            2|2
            01:46:41.328 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:46:41.328 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:46:41.329 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%14,20%3,4%1,3%be,s%9,22,17,74,23%0,0%
            01:46:41.329 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%14,20%3,4%1,3%be,s%22,43,58,53,65%0,0%
            01:46:42.590 - [ INFO ] > { DATA IN } : %xt%s%u#h%137%
            01:46:42.590 - [ INFO ] > { DATA OUT } : %xt%h%137%
            01:46:44.178 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:46:45.487 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:46:45.488 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%5,9,15%9,22,17,74,23%null%
            01:46:45.488 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%5,9,15%22,43,58,53,65%null%
            01:46:48.202 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%1%6%
            01:46:48.202 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:46:48.203 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:46:50.671 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%9%
            01:46:50.671 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%1,9%2%
            01:46:50.672 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%1,9%2%
            01:46:50.672 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%s%9,22,17,74,23%
            01:46:50.672 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%s%22,43,58,53,65%
            01:46:51.562 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%2%
            1|2
            01:46:51.563 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:46:51.563 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:46:52.884 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%2%
            2|2
            01:46:52.884 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:46:52.885 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:46:52.885 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%17,58%2,4%1,3%be,s%9,22,43,74,23%0,0%
            01:46:52.885 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%17,58%2,4%1,3%be,s%22,43,72,53,65%0,0%
            01:46:55.760 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:46:57.237 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:46:57.237 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%6,7,11%9,22,43,74,23%null%
            01:46:57.237 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%6,7,11%22,43,72,53,65%null%
            01:46:59.843 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%0%1%
            01:46:59.844 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%0%1%
            01:46:59.844 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%0%1%
            01:47:01.546 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%11%
            01:47:01.546 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%0%11,9%2%
            01:47:01.546 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%0%11,9%2%
            01:47:01.547 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%9,22,43,74,23%
            01:47:01.547 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%22,43,72,53,65%
            01:47:02.503 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            1|2
            01:47:02.504 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:47:02.504 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:47:03.241 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%2%
            2|2
            01:47:03.241 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:47:03.241 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:47:03.242 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%74,72%2,3%3,1%be,f%9,22,43,1,23%0,0%
            01:47:03.242 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%74,72%2,3%3,1%be,f%22,43,74,53,65%0,0%
            01:47:04.457 - [ INFO ] > { DATA IN } : %xt%s%u#h%137%
            01:47:04.457 - [ INFO ] > { DATA OUT } : %xt%h%137%
            01:47:06.594 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:47:08.774 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:47:08.775 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%6,15,3%9,22,43,1,23%null%
            01:47:08.775 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%6,15,3%22,43,74,53,65%null%
            01:47:11.163 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%1%6%
            01:47:11.164 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:47:11.164 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:47:12.821 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%15%
            01:47:12.822 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%11,15%2%
            01:47:12.822 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%11,15%2%
            01:47:12.822 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%9,22,43,1,23%
            01:47:12.822 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%22,43,74,53,65%
            01:47:15.365 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%2%
            1|2
            01:47:15.365 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:47:15.366 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:47:16.450 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            2|2
            01:47:16.450 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:47:16.451 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:47:16.451 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%1,74%1,3%1,3%be,f%9,22,43,74,23%0,0%
            01:47:16.451 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%1,74%1,3%1,3%be,f%22,43,20,53,65%0,0%
            01:47:18.937 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:47:20.135 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:47:20.136 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%4,15,7%9,22,43,74,23%null%
            01:47:20.136 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%4,15,7%22,43,20,53,65%null%
            01:47:23.308 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%0%5%
            01:47:23.308 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%0%1%
            01:47:23.309 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%0%1%
            01:47:25.616 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%15%
            01:47:25.616 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%0%15,15%2%
            01:47:25.616 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%0%15,15%2%
            01:47:25.616 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%9,22,43,74,23%
            01:47:25.617 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%22,43,20,53,65%
            01:47:28.096 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            1|2
            01:47:28.097 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:47:28.097 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:47:28.940 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            2|2
            01:47:28.941 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:47:28.941 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:47:28.941 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%74,53%1,2%3,1%be,f%9,22,43,6,23%0,0%
            01:47:28.942 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%74,53%1,2%3,1%be,f%22,43,20,74,65%0,0%
            01:47:31.507 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:47:32.881 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:47:32.882 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%4,3,11%9,22,43,6,23%null%
            01:47:32.882 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%4,3,11%22,43,20,74,65%null%
            01:47:35.565 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%1%5%
            01:47:35.566 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:47:35.566 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:47:36.727 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%3%
            01:47:36.728 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%15,3%2%
            01:47:36.728 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%15,3%2%
            01:47:36.728 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%9,22,43,6,23%
            01:47:36.729 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%22,43,20,74,65%
            01:47:37.961 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            1|2
            01:47:37.961 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:47:37.961 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:47:39.070 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            2|2
            01:47:39.070 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:47:39.071 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:47:39.072 - [ INFO ] > { DATA OUT } : %xt%zm%137%lz%0%
            01:47:39.072 - [ INFO ] > { DATA OUT } : %xt%zm%137%lz%0%
            01:47:39.072 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%6,74%0,2%1,3%be,f%9,22,43,26,23%2,0%
            01:47:39.073 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%6,74%0,2%1,3%be,f%22,43,20,60,65%2,0%
            01:47:39.073 - [ INFO ] > { DATA OUT } : %xt%cjsi%137%%1%10%7%
            01:47:39.073 - [ INFO ] > { DATA OUT } : %xt%zm%137%zo%2,0%
            01:47:42.498 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:47:42.498 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%6,9,13%22,43,20,60,65%null%
            01:47:42.598 - [ INFO ] > { DATA IN } : %xt%s%u#h%137%
            01:47:42.599 - [ INFO ] > { DATA OUT } : %xt%h%137%
            ''')

    def do_fire1(self, args):
        print "Card-Jitsu Fire SEAT ID 1"
        print (
            '''
            01:44:01.028 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:44:01.028 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:44:01.028 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%20,51%3,3%1,4%be,f%81,60,6,82,17%0,0%
            01:44:01.028 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%20,51%3,3%1,4%be,f%43,20,14,17,6%0,0%
            01:44:03.520 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:44:04.388 - [ INFO ] > { DATA IN } : %xt%s%u#h%137%
            01:44:04.391 - [ INFO ] > { DATA OUT } : %xt%h%137%
            01:44:05.288 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:44:05.288 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%4,1,9%81,60,6,82,17%null%
            01:44:05.289 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%4,1,9%43,20,14,17,6%null%
            01:44:07.911 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%1%6%
            01:44:07.912 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:44:07.912 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:44:12.422 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%1%
            01:44:12.422 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%0,1%2%
            01:44:12.423 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%0,1%2%
            01:44:12.423 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%s%81,60,6,82,17%
            01:44:12.423 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%s%43,20,14,17,6%
            01:44:13.724 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%1%
            1|2
            01:44:13.725 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:44:13.725 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:44:14.381 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%0%
            2|2
            01:44:14.382 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:44:14.382 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:44:14.382 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%81,20%3,2%3,1%be,s%9,60,6,82,17%0,0%
            01:44:14.382 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%81,20%3,2%3,1%be,s%43,89,14,17,6%0,0%
            01:44:17.378 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:44:19.635 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:44:19.636 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%5,5,11%9,60,6,82,17%null%
            01:44:19.636 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%5,5,11%43,89,14,17,6%null%
            01:44:22.053 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%0%5%
            01:44:22.053 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%0%1%
            01:44:22.053 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%0%1%
            01:44:35.900 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%11%
            01:44:35.900 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%0%11,1%2%
            01:44:35.900 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%0%11,1%2%
            01:44:35.900 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%9,60,6,82,17%
            01:44:35.901 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%f%43,89,14,17,6%
            01:44:37.530 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%2%
            1|2
            01:44:37.531 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:44:37.531 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:44:38.698 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%4%
            2|2
            01:44:38.698 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:44:38.699 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:44:38.699 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%6,6%3,2%3,2%be,f%9,60,60,82,17%0,0%
            01:44:38.699 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%6,6%3,2%3,2%be,f%43,89,14,17,1%0,0%
            01:44:41.386 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:44:42.388 - [ INFO ] > { DATA IN } : %xt%s%u#h%137%
            01:44:42.388 - [ INFO ] > { DATA OUT } : %xt%h%137%
            01:44:42.553 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:44:42.553 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%5,6,12%9,60,60,82,17%null%
            01:44:42.553 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%5,6,12%43,89,14,17,1%null%
            01:44:46.125 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%1%1%
            01:44:46.126 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:44:46.126 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:44:51.567 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%12%
            01:44:51.567 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%11,12%2%
            01:44:51.568 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%11,12%2%
            01:44:51.568 - [ INFO ] > { DATA OUT } : %xt%zm%137%ct%1%
            01:44:51.568 - [ INFO ] > { DATA OUT } : %xt%zm%137%ct%1%
            01:44:52.947 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ct%w%
            01:44:52.948 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%w%9,60,60,82,17%
            01:44:52.948 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%w%43,89,14,17,1%
            01:44:53.695 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%1%
            1|2
            01:44:53.696 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:44:53.696 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:44:54.562 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            2|2
            01:44:54.562 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:44:54.562 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:44:54.562 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%82,89%2,2%1,3%be,w%9,60,60,22,17%0,0%
            01:44:54.563 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%82,89%2,2%1,3%be,w%43,60,14,17,1%0,0%
            01:44:57.249 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:44:59.617 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:44:59.617 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%2,13,9%9,60,60,22,17%null%
            01:44:59.617 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%2,13,9%43,60,14,17,1%null%
            01:45:01.948 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%0%6%
            01:45:01.948 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%0%1%
            01:45:01.948 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%0%1%
            01:45:03.793 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%13%
            01:45:03.794 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%0%13,12%2%
            01:45:03.794 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%0%13,12%2%
            01:45:03.794 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%w%9,60,60,22,17%
            01:45:03.795 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%w%43,60,14,17,1%
            01:45:04.422 - [ INFO ] > { DATA IN } : %xt%s%u#h%137%
            01:45:04.422 - [ INFO ] > { DATA OUT } : %xt%h%137%
            01:45:04.941 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            1|2
            01:45:04.942 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:45:04.942 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:45:06.177 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%2%
            2|2
            01:45:06.177 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:45:06.178 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:45:06.178 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%22,14%2,1%3,1%be,w%9,60,60,82,17%0,0%
            01:45:06.178 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%22,14%2,1%3,1%be,w%43,60,23,17,1%0,0%
            01:45:08.747 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:45:10.386 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:45:10.386 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%5,1,7%9,60,60,82,17%null%
            01:45:10.387 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%1%5,1,7%43,60,23,17,1%null%
            01:45:12.632 - [ INFO ] > { DATA IN } : %xt%z%zm%137%is%1%6%
            01:45:12.633 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:45:12.633 - [ INFO ] > { DATA OUT } : %xt%zm%137%is%1%1%
            01:45:14.047 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cb%1%
            01:45:14.048 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%13,1%2%
            01:45:14.048 - [ INFO ] > { DATA OUT } : %xt%zm%137%ub%1%13,1%2%
            01:45:14.048 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%s%9,60,60,82,17%
            01:45:14.048 - [ INFO ] > { DATA OUT } : %xt%zm%137%sb%bt%0,1%s%43,60,23,17,1%
            01:45:15.196 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%1%
            1|2
            01:45:15.197 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:45:15.197 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%1%
            01:45:15.940 - [ INFO ] > { DATA IN } : %xt%z%zm%137%cc%3%
            2|2
            01:45:15.941 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:45:15.941 - [ INFO ] > { DATA OUT } : %xt%zm%137%ic%0%
            01:45:15.941 - [ INFO ] > { DATA OUT } : %xt%zm%137%lz%1%
            01:45:15.942 - [ INFO ] > { DATA OUT } : %xt%zm%137%lz%1%
            01:45:15.942 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%82,60%2,0%3,1%be,s%9,60,60,112,17%0,2%
            01:45:15.942 - [ INFO ] > { DATA OUT } : %xt%zm%137%rb%0,1%82,60%2,0%3,1%be,s%43,20,23,17,1%0,2%
            01:45:15.942 - [ INFO ] > { DATA OUT } : %xt%cjsi%137%%1%10%7%
            01:45:15.942 - [ INFO ] > { DATA OUT } : %xt%zm%137%zo%1,2%
            01:45:19.123 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%1%
            01:45:20.855 - [ INFO ] > { DATA IN } : %xt%z%zm%137%ir%0%
            01:45:20.855 - [ INFO ] > { DATA OUT } : %xt%zm%137%nt%0%2,15,11%9,60,60,112,17%null%
            01:45:33.196 - [ INFO ] > { DATA IN } : %xt%z%lz%137%
            ''')

    #-----------#
    # Protocols #
    #-----------#

    def do_protocols(self, args):
        print(
            '''
            var PLAY_EXT = "s";
            var GAME_EXT = "z";
            var NAVIGATION = "j";
            var PLAYER_HANDLER = "u";
            var ITEM_HANDLER = "i";
            var IGNORE_HANDLER = "n";
            var BUDDY_HANDLER = "b";
            var TOY_HANDLER = "t";
            var TABLE_HANDLER = "a";
            var IGLOO_HANDLER = "g";
            var PET_HANDLER = "p";
            var MESSAGE_HANDLER = "m";
            var MAIL_HANDLER = "l";
            var SURVEY_HANDLER = "e";
            var WADDLE = "w";
            var SETTING_HANDLER = "s";
            var MODERATION_HANDLER = "o";
            var NINJA_HANDLER = "ni";
            var ROOM_HANDLER = "r";
            var REDEMPTION = "red";
            var REDEMPTION_JOIN_WORLD = "rjs";
            var HANDLE_LOGIN = "l";
            var HANDLE_ALERT = "a";
            var HANDLE_ERROR = "e";
            var GET_BUDDY_LIST = "gb";
            var GET_IGNORE_LIST = "gn";
            var GET_PLAYER = "gp";
            var GET_ROOM_LIST = "gr";
            var GET_TABLE = "gt";
            var JOIN_WORLD = "js";
            var JOIN_ROOM = "jr";
            var REFRESH_ROOM = "grs";
            var LOAD_PLAYER = "lp";
            var ADD_PLAYER = "ap";
            var REMOVE_PLAYER = "rp";
            var UPDATE_PLAYER = "up";
            var PLAYER_MOVE = "sp";
            var PLAYER_FRAME = "sf";
            var PLAYER_ACTION = "sa";
            var OPEN_BOOK = "at";
            var CLOSE_BOOK = "rt";
            var THROW_BALL = "sb";
            var JOIN_GAME = "jg";
            var SEND_MESSAGE = "sm";
            var SEND_BLOCKED_MESSAGE = "mm";
            var SEND_EMOTE = "se";
            var SEND_JOKE = "sj";
            var SEND_SAFE_MESSAGE = "ss";
            var SEND_LINE_MESSAGE = "sl";
            var SEND_QUICK_MESSAGE = "sq";
            var SEND_TOUR_GUIDE_MESSAGE = "sg";
            var COIN_DIG_UPDATE = "cdu";
            var GET_INVENTORY_LIST = "gi";
            var MAIL_START_ENGINE = "mst";
            var GET_MAIL = "mg";
            var SEND_MAIL = "ms";
            var RECEIVE_MAIL = "mr";
            var DELETE_MAIL = "md";
            var DELETE_MAIL_FROM_PLAYER = "mdp";
            var GET_MAIL_DETAILS = "mgd";
            var MAIL_CHECKED = "mc";
            var GAME_OVER = "zo";
            var BUY_INVENTORY = "ai";
            var CHECK_INVENTORY = "qi";
            var ADD_IGNORE = "an";
            var REMOVE_IGNORE = "rn";
            var REMOVE_BUDDY = "rb";
            var REQUEST_BUDDY = "br";
            var ACCEPT_BUDDY = "ba";
            var BUDDY_ONLINE = "bon";
            var BUDDY_OFFLINE = "bof";
            var FIND_BUDDY = "bf";
            var GET_PLAYER_OBJECT = "gp";
            var REPORT_PLAYER = "r";
            var UPDATE_PLAYER_COLOUR = "upc";
            var UPDATE_PLAYER_HEAD = "uph";
            var UPDATE_PLAYER_FACE = "upf";
            var UPDATE_PLAYER_NECK = "upn";
            var UPDATE_PLAYER_BODY = "upb";
            var UPDATE_PLAYER_HAND = "upa";
            var UPDATE_PLAYER_FEET = "upe";
            var UPDATE_PLAYER_FLAG = "upl";
            var UPDATE_PLAYER_PHOTO = "upp";
            var UPDATE_PLAYER_REMOVE = "upr";
            var GET_FURNITURE_LIST = "gf";
            var UPDATE_ROOM = "up";
            var UPDATE_FLOOR = "ag";
            var UPDATE_IGLOO_TYPE = "au";
            var UNLOCK_IGLOO = "or";
            var LOCK_IGLOO = "cr";
            var UPDATE_IGLOO_MUSIC = "um";
            var GET_IGLOO_DETAILS = "gm";
            var JOIN_PLAYER_IGLOO = "jp";
            var SAVE_IGLOO_FURNITURE = "ur";
            var GET_IGLOO_LIST = "gr";
            var BUY_FURNITURE = "af";
            var SEND_IGLOO = "sig";
            var GET_OWNED_IGLOOS = "go";
            var ACTIVATE_IGLOO = "ao";
            var GET_MY_PLAYER_PUFFLES = "pgu";
            var GET_PLAYER_PUFFLES = "pg";
            var PUFFLE_FRAME = "ps";
            var PUFFLE_MOVE = "pm";
            var REST_PUFFLE = "pr";
            var BATH_PUFFLE = "pb";
            var PLAY_PUFFLE = "pp";
            var FEED_PUFFLE = "pf";
            var WALK_PUFFLE = "pw";
            var TREAT_PUFFLE = "pt";
            var INTERACTION_PLAY = "ip";
            var INTERACTION_REST = "ir";
            var INTERACTION_FEED = "if";
            var PUFFLE_INIT_INTERACTION_PLAY = "pip";
            var PUFFLE_INIT_INTERACTION_REST = "pir";
            var ADOPT_PUFFLE = "pn";
            var UPDATE_TABLE = "ut";
            var GET_TABLE_POPULATION = "gt";
            var JOIN_TABLE = "jt";
            var LEAVE_TABLE = "lt";
            var UPDATE_WADDLE = "uw";
            var GET_WADDLE_POPULATION = "gw";
            var JOIN_WADDLE = "jw";
            var LEAVE_WADDLE = "lw";
            var START_WADDLE = "sw";
            var SEND_WADDLE = "jx";
            var SPY_PHONE_REQUEST = "spy";
            var HEARTBEAT = "h";
            var TIMEOUT = "t";
            var MODERATOR_ACTION = "ma";
            var KICK = "k";
            var MUTE = "m";
            var BAN = "b";
            var SEND_MASCOT_MESSAGE = "sma";
            var DONATE = "dc";
            var POLL = "spl";
            var CONNECTION_LOST = "con";
            var GET_CARDS = "gcd";
            var GET_NINJA_LEVEL = "gnl";
            var GET_FIRE_LEVEL = "gfl";
            var GET_WATER_LEVEL = "gwl";
            var GET_NINJA_RANKS = "gnr";
            var GET_LAST_REVISION = "glr";
            ''')

    #----------#
    # Airtower #
    #----------#

    def do_airtower(self, args):
        print(
            '''
            AIRTOWER.addListener(AIRTOWER.SEND_MESSAGE, handleSendMessage);
            AIRTOWER.addListener(AIRTOWER.SEND_BLOCKED_MESSAGE, handleBlockedMessage);
            AIRTOWER.addListener(AIRTOWER.SEND_SAFE_MESSAGE, handleSafeMessage);
            AIRTOWER.addListener(AIRTOWER.SEND_LINE_MESSAGE, handleLineMessage);
            AIRTOWER.addListener(AIRTOWER.SEND_QUICK_MESSAGE, handleSendQuickMessage);
            AIRTOWER.addListener(AIRTOWER.SEND_TOUR_GUIDE_MESSAGE, handleTourGuideMessage);
            AIRTOWER.addListener(AIRTOWER.SEND_EMOTE, handleSendEmote);
            AIRTOWER.addListener(AIRTOWER.SEND_JOKE, handleSendJoke);
            AIRTOWER.addListener(AIRTOWER.SEND_MASCOT_MESSAGE, handleMascotMessage);
            AIRTOWER.addListener(AIRTOWER.COIN_DIG_UPDATE, handleGetCoinReward);
            AIRTOWER.addListener(AIRTOWER.GET_INVENTORY_LIST, handleMyGetInventoryList);
            AIRTOWER.addListener(AIRTOWER.GET_BUDDY_LIST, handleGetBuddyListFromServer);
            AIRTOWER.addListener(AIRTOWER.GET_IGNORE_LIST, handleGetIgnoreListFromServer);
            AIRTOWER.addListener(AIRTOWER.REMOVE_BUDDY, handleRemoveBuddyPlayer);
            AIRTOWER.addListener(AIRTOWER.REQUEST_BUDDY, handleBuddyRequest);
            AIRTOWER.addListener(AIRTOWER.ACCEPT_BUDDY, handleBuddyAccept);
            AIRTOWER.addListener(AIRTOWER.BUDDY_ONLINE, handleBuddyOnline);
            AIRTOWER.addListener(AIRTOWER.BUDDY_OFFLINE, handleBuddyOffline);
            AIRTOWER.addListener(AIRTOWER.FIND_BUDDY, handleGetPlayerLocationById);
            AIRTOWER.addListener(AIRTOWER.GAME_OVER, handleGameOver);
            AIRTOWER.addListener(AIRTOWER.BUY_INVENTORY, handleBuyInventory);
            AIRTOWER.addListener(AIRTOWER.CHECK_INVENTORY, handleCheckInventory);
            AIRTOWER.addListener(AIRTOWER.GET_PLAYER_OBJECT, handleLoadPlayerObject);
            AIRTOWER.addListener(AIRTOWER.GET_FURNITURE_LIST, handleGetFurnitureListFromServer);
            AIRTOWER.addListener(AIRTOWER.GET_IGLOO_DETAILS, handleGetPlayerIgloo);
            AIRTOWER.addListener(AIRTOWER.GET_IGLOO_LIST, handleLoadPlayerIglooList);
            AIRTOWER.addListener(AIRTOWER.GET_OWNED_IGLOOS, handleGetOwnedIgloos);
            AIRTOWER.addListener(AIRTOWER.BUY_FURNITURE, handleSendBuyFurniture);
            AIRTOWER.addListener(AIRTOWER.UPDATE_FLOOR, handleSendBuyIglooFloor);
            AIRTOWER.addListener(AIRTOWER.UPDATE_IGLOO_TYPE, handleSendBuyIglooType);
            AIRTOWER.addListener(AIRTOWER.MODERATOR_ACTION, handleModeratorAction);
            AIRTOWER.addListener(AIRTOWER.LOAD_PLAYER, handleLoadPlayer);
            AIRTOWER.addListener(AIRTOWER.JOIN_ROOM, handleJoinRoom);
            AIRTOWER.addListener(AIRTOWER.JOIN_GAME, handleJoinGame);
            AIRTOWER.addListener(AIRTOWER.REFRESH_ROOM, handleRefreshRoom);
            AIRTOWER.addListener(AIRTOWER.ADD_PLAYER, handleAddPlayerToRoom);
            AIRTOWER.addListener(AIRTOWER.REMOVE_PLAYER, handleRemovePlayerFromRoom);
            AIRTOWER.addListener(AIRTOWER.PLAYER_MOVE, handleSendPlayerMove);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_COLOUR, handleSendUpdatePlayerColour);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_HEAD, handleSendUpdatePlayerHead);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_FACE, handleSendUpdatePlayerFace);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_NECK, handleSendUpdatePlayerNeck);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_BODY, handleSendUpdatePlayerBody);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_HAND, handleSendUpdatePlayerHand);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_FEET, handleSendUpdatePlayerFeet);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_FLAG, handleSendUpdatePlayerFlag);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_PHOTO, handleSendUpdatePlayerPhoto);
            AIRTOWER.addListener(AIRTOWER.UPDATE_PLAYER_REMOVE, handleSendClearPaperdoll);
            AIRTOWER.addListener(AIRTOWER.PLAYER_FRAME, handleSendPlayerFrame);
            AIRTOWER.addListener(AIRTOWER.PLAYER_ACTION, handleUpdatePlayerAction);
            AIRTOWER.addListener(AIRTOWER.OPEN_BOOK, handleOpenPlayerBook);
            AIRTOWER.addListener(AIRTOWER.CLOSE_BOOK, handleClosePlayerBook);
            AIRTOWER.addListener(AIRTOWER.THROW_BALL, handlePlayerThrowBall);
            AIRTOWER.addListener(AIRTOWER.UPDATE_TABLE, handleUpdateTableById);
            AIRTOWER.addListener(AIRTOWER.GET_TABLE_POPULATION, handleGetTablesPopulationById);
            AIRTOWER.addListener(AIRTOWER.JOIN_TABLE, handleSendJoinTableById);
            AIRTOWER.addListener(AIRTOWER.LEAVE_TABLE, handleLeaveTable);
            AIRTOWER.addListener(AIRTOWER.UPDATE_WADDLE, handleUpdateWaddle);
            AIRTOWER.addListener(AIRTOWER.GET_WADDLE_POPULATION, handleGetWaddlesPopulationById);
            AIRTOWER.addListener(AIRTOWER.JOIN_WADDLE, handleSendJoinWaddleById);
            AIRTOWER.addListener(AIRTOWER.LEAVE_WADDLE, handleLeaveWaddle);
            AIRTOWER.addListener(AIRTOWER.START_WADDLE, startWaddle);
            AIRTOWER.addListener(AIRTOWER.SEND_WADDLE, handleJoinWaddle);
            AIRTOWER.addListener(AIRTOWER.MAIL_START_ENGINE, handleStartMailEngine);
            AIRTOWER.addListener(AIRTOWER.GET_MAIL, handleGetMail);
            AIRTOWER.addListener(AIRTOWER.RECEIVE_MAIL, handleRecieveMailItem);
            AIRTOWER.addListener(AIRTOWER.SEND_MAIL, handleSendMailItem);
            AIRTOWER.addListener(AIRTOWER.DELETE_MAIL_FROM_PLAYER, handleDeleteMailFromUser);
            AIRTOWER.addListener(AIRTOWER.DONATE, handleDonateToCharity);
            AIRTOWER.addListener(AIRTOWER.GET_CARDS, handleGetCards);
            AIRTOWER.addListener(AIRTOWER.GET_NINJA_LEVEL, handleGetNinjaLevel);
            AIRTOWER.addListener(AIRTOWER.GET_FIRE_LEVEL, handleGetFireLevel);
            AIRTOWER.addListener(AIRTOWER.GET_WATER_LEVEL, handleGetWaterLevel);
            AIRTOWER.addListener(AIRTOWER.GET_NINJA_RANKS, handleGetNinjaRanks);
            ''')

if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = '> '
    print "Commands: | navigation | exit |"
    prompt.cmdloop('Starting ProtocolCP.py => By Zaseth @@ 2017.')