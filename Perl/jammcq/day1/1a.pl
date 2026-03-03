#!/usr/bin/perl -w

use strict;

my $filename   = $ARGV[0] or die( "Must specify filename as the only argument!\n" );
my $current    = 50;
my $zero_count = 0;

open( my $FH, '<', $filename ) or die( "Failed to pen $filename: $!\n" );

while( my $line = <$FH> ){
  if( my ( $dir, $count ) = $line =~ m/^([LR])(\d+)$/ ){

    if( $dir eq 'L' ){
      $current -= $count;
      $current += 100 while( $current < 0 );
    }
    elsif( $dir eq 'R' ){
      $current += $count;
      $current -= 100 while( $current >= 100 );
    }

    $zero_count++ if( $current == 0 );
  }
}

print( "The combination is $zero_count\n" );
