                    <div id="boardcontents_placeholder">
                    <div class="row">
                    <!-- this place will show the actual contents of the blackboard. 
                    It will be reloaded automatically from the server -->
                        <div class="card shadow mb-4 w-100">
                            <div class="card-header py-3">
                              <h6 class="font-weight-bold ">Logical Server Time: {{server_title}}</h6>
                              <h6 class="font-weight-bold text-primary"> Blackboard content: {{ len(board_dict) }}</h6>
                            </div>
                            <div class="card-body">
                                <input style = "border:0; font-weight: bold;" type="text" name="id" value="ID" readonly/>
                                <input style = "border:0; font-weight: bold;" type="text" name="vc" value="Logical Time" readonly/>
                                <input style = "border:0; font-weight: bold;" type="text" name="entry" value="Entry" size="50%%" readonly />
                                % for board_entry, dataObj in board_dict:
                                    <form class="entryform" target="noreload" method="post" action="/board/{{board_entry}}/">
                                        <input style = "border:0" type="text" name="id" value="{{board_entry}}" readonly disabled /> <!-- disabled field won’t be sent -->
                                        <input style = "border:0" type="text" name="vc" value="{{dataObj.vector_clock}}" readonly disabled/>
                                        <input type="text" name="entry" value="{{dataObj.text}}" size="50%%" />
                                        <button type="submit" name="delete" value="0">Modify</button>
                                        <button type="submit" name="delete" value="1">X</button>
                                    </form>
                                %end
                            </div>
                        </div>
                    </div>
                    </div>