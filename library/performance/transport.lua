-- TRN-02…04. Transporte sin repertorio. Candidatos precalculados por segundo.
local function tr_control(value,default)
 if type(value)~='number' or value~=value then return default end
 return math.max(0,math.min(1,value))
end
local function tr_new(duration)
 return {duration=duration,gain=0,playing=true,lastSeek=nil,rewindHigh=false,pending=nil,seeks=0}
end
local function tr_upper(notes,time)
 local lo,hi=1,#notes+1
 while lo<hi do local mid=math.floor((lo+hi)/2);if notes[mid] and notes[mid][1]<=time then lo=mid+1 else hi=mid end end
 return lo
end
local function tr_active(notes,buckets,time,polyphonic,speed)
 local result={}
 for _,i in ipairs(buckets[math.floor(time)+1] or {}) do
  local n=notes[i]
  if n[1]<=time and time<n[2] then
   if polyphonic then
    local hz=440*2^((n[3]-69)/12)
    result[#result+1]={n=n,phase=((time-n[1])*hz/speed)%1}
   else result[#result+1]=n end
  end
 end
 return result,tr_upper(notes,time)
end
local function tr_tick(tr,rate,position,pause,rewind,onSeek)
 local j=tr_control(position,0);local k=tr_control(pause,0);local l=tr_control(rewind,0)
 if tr.lastSeek==nil or math.abs(j-tr.lastSeek)>=.0005 then tr.pending=j*tr.duration;tr.lastSeek=j end
 if k>.6 then tr.playing=false elseif k<.4 then tr.playing=true end
 if l>.6 and not tr.rewindHigh then tr.pending=0;tr.rewindHigh=true
 elseif l<.4 then tr.rewindHigh=false end
 local increment=1/(rate*.02)
 if tr.pending~=nil or not tr.playing then tr.gain=math.max(0,tr.gain-increment)
 else tr.gain=math.min(1,tr.gain+increment) end
 if tr.pending~=nil and tr.gain==0 then
  local target=tr.pending;tr.pending=nil;tr.seeks=tr.seeks+1;tr.lastTarget=target
  onSeek(target)
 end
end
