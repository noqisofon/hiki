#!/usr/bin/env ruby
# $Id: hiki.cgi,v 1.23 2004-12-14 16:12:32 fdiary Exp $
# Copyright (C) 2002-2004 TAKEUCHI Hitoshi <hitoshi@namaraii.com>

BEGIN { $defout.binmode }

$SAFE     = 1
$KCODE    = 'e'

begin
  if FileTest::symlink?( __FILE__ ) then
    org_path = File::dirname( File::readlink( __FILE__ ) )
  else
    org_path = File::dirname( __FILE__ )
  end
  $:.unshift( org_path.untaint )

  require 'hiki/config'
  conf = Hiki::Config::new

  cgi = CGI::new

  db = Hiki::HikiDB::new( conf )
  db.open_db {
    cmd = Hiki::Command::new( cgi, db, conf )
    cmd.dispatch
  }
rescue Exception
  if cgi then
    print cgi.header( 'type' => 'text/plain' )
  else
    print "Content-Type: text/plain\n\n"
  end
  puts "#$! (#{$!.class})\n"
  puts $@.join( "\n" )
end
